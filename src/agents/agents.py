"""
Agent implementations.

Patterns implemented (named here + in README.md):

1. ROUTER pattern            -> RouterAgent.classify()
2. REACT / TOOL-USE pattern  -> SupportAgent.handle()  (search-kb tool loop)
3. TOOL-USE + REFLECTION     -> InventoryAgent.handle() (self-critique step)
4. ORCHESTRATOR-WORKER /
   PLANNING-DECOMPOSITION    -> OrchestratorAgent.handle_query()

Agent-to-agent communication uses the AgentMessage/MessageBus protocol in
protocol.py — every hop between Orchestrator, Router, Support, and
Inventory agents is a structured message, not a bare function call.
"""

from __future__ import annotations

from typing import Any, Dict, List, TYPE_CHECKING

from src.agents.protocol import AgentMessage, MessageBus
from src.models.clients import call_llm
from src.tools.inventory_tool import lookup_stock, list_low_stock

if TYPE_CHECKING:  # pragma: no cover - import only used for type hints
    from src.rag.pipeline import RAGPipeline


# ---------------------------------------------------------------------------
# 1. ROUTER AGENT
# ---------------------------------------------------------------------------
class RouterAgent:
    """Classifies an incoming query into one or more downstream worker
    agents. Uses the cheapest/fastest model in the registry (Groq 8B)
    because this is a low-complexity classification task where latency
    matters more than deep reasoning."""

    VALID_ROUTES = {"support", "inventory", "both"}

    def classify(self, bus: MessageBus, query: str) -> str:
        system = (
            "You are an intent router for a spice & tea export company's "
            "internal assistant. Classify the user's message into exactly one "
            "label: 'support' (product info, policies, shipping, payment, "
            "certification, FAQ-type questions), 'inventory' (stock levels, "
            "reorder, availability), or 'both' (needs both). "
            "Reply with only the single label word."
        )
        bus.send(AgentMessage(
            sender="orchestrator", receiver="router", type="classify",
            content=query,
        ))
        resp = call_llm("router", system, query, max_tokens=10)
        label = (resp.text or "").strip().lower()
        route = next((r for r in self.VALID_ROUTES if r in label), "support")
        bus.send(AgentMessage(
            sender="router", receiver="orchestrator", type="route_decision",
            content=route,
            context={"provider": resp.provider, "model": resp.model,
                     "latency_s": round(resp.latency_s, 3), "error": resp.error},
        ))
        return route


# ---------------------------------------------------------------------------
# 2. SUPPORT AGENT (ReAct-style: retrieve -> observe -> answer, grounded RAG)
# ---------------------------------------------------------------------------
class SupportAgent:
    """Handles product/policy/FAQ questions. Implements a simplified ReAct
    loop: Thought (what to search for) -> Action (search_kb tool) ->
    Observation (retrieved chunks) -> Answer, grounded strictly in the
    retrieved context. Uses the strongest reasoning model (OpenRouter)
    since answer quality/faithfulness to policy text matters most here."""

    def __init__(self, rag: "RAGPipeline"):
        self.rag = rag

    def handle(self, bus: MessageBus, query: str) -> Dict[str, Any]:
        bus.send(AgentMessage(
            sender="orchestrator", receiver="support", type="subtask",
            content=query,
        ))

        # Action: search_kb tool
        retrieved = self.rag.retrieve(query, k=4)
        context_block = "\n\n".join(
            f"[Source: {r.chunk.source} | relevance={r.score:.2f}]\n{r.chunk.text}"
            for r in retrieved
        )

        system = (
            "You are the customer/staff support agent for Serendib Spice & "
            "Tea Traders, a Sri Lankan spice and tea export company. Answer "
            "ONLY using the provided context from company documents. If the "
            "context does not contain the answer, say you don't have that "
            "information on file rather than guessing. Cite the source "
            "filename(s) you used in parentheses at the end of relevant "
            "sentences. Be concise and business-appropriate."
        )
        user = f"Context:\n{context_block}\n\nQuestion: {query}"
        resp = call_llm("synthesis", system, user, max_tokens=500)

        result = {
            "answer": resp.text or "(no response — check API key / connectivity)",
            "sources": sorted({r.chunk.source for r in retrieved}),
            "provider": resp.provider,
            "model": resp.model,
            "latency_s": round(resp.latency_s, 3),
            "error": resp.error,
        }
        bus.send(AgentMessage(
            sender="support", receiver="orchestrator", type="subtask_result",
            content=result["answer"],
            context={"sources": result["sources"], "provider": result["provider"],
                     "model": result["model"], "latency_s": result["latency_s"]},
        ))
        return result


# ---------------------------------------------------------------------------
# 3. INVENTORY AGENT (tool-use + reflection/self-critique)
# ---------------------------------------------------------------------------
class InventoryAgent:
    """Handles stock/reorder questions. Calls the inventory tool, drafts a
    recommendation, then runs a reflection pass where the model critiques
    its own draft against the raw tool data before finalising — catching
    cases like recommending a reorder quantity below the product's MOQ."""

    def handle(self, bus: MessageBus, query: str) -> Dict[str, Any]:
        bus.send(AgentMessage(
            sender="orchestrator", receiver="inventory", type="subtask",
            content=query,
        ))

        stock = lookup_stock(query)
        low_stock = list_low_stock()

        if not stock.found:
            result = {
                "answer": (
                    "I couldn't match that to a product in the inventory system. "
                    f"Currently low-stock items are: "
                    f"{', '.join(i['product'] for i in low_stock) or 'none'}."
                ),
                "provider": None, "model": None, "latency_s": 0.0, "error": None,
            }
            bus.send(AgentMessage(sender="inventory", receiver="orchestrator",
                                   type="subtask_result", content=result["answer"]))
            return result

        tool_facts = (
            f"Product: {stock.product}\nSKU: {stock.sku}\n"
            f"Current stock: {stock.stock_kg} kg\n"
            f"Reorder point: {stock.reorder_point_kg} kg\n"
            f"MOQ for reordering from supplier: {stock.moq_kg} kg\n"
            f"Below reorder point: {stock.below_reorder_point}"
        )

        # --- draft ---
        draft_system = (
            "You are the inventory/operations agent for a spice & tea export "
            "company. Given raw stock data, write a short internal status "
            "note: current stock, whether it's below reorder point, and (if "
            "so) a concrete reorder recommendation with quantity in kg."
        )
        draft_resp = call_llm("rerank_reflect", draft_system, tool_facts, max_tokens=250)
        draft = draft_resp.text or ""

        # --- reflection / self-critique ---
        critique_system = (
            "You are reviewing an inventory recommendation before it goes to "
            "the operations manager. Check it against the raw data: is the "
            "reorder quantity (if any) at least the stated MOQ? Is the stock "
            "status correctly stated? If the draft is correct, restate it "
            "cleanly. If it has an error (e.g. proposes a quantity below "
            "MOQ, or misreads the stock status), correct it. Output only the "
            "final corrected note, no meta-commentary."
        )
        critique_user = f"Raw data:\n{tool_facts}\n\nDraft note:\n{draft}"
        final_resp = call_llm("rerank_reflect", critique_system, critique_user, max_tokens=250)
        final_answer = final_resp.text or draft

        result = {
            "answer": final_answer,
            "draft_before_reflection": draft,
            "tool_data": tool_facts,
            "provider": final_resp.provider,
            "model": final_resp.model,
            "latency_s": round(draft_resp.latency_s + final_resp.latency_s, 3),
            "error": final_resp.error or draft_resp.error,
        }
        bus.send(AgentMessage(
            sender="inventory", receiver="orchestrator", type="subtask_result",
            content=result["answer"],
            context={"draft_before_reflection": draft, "tool_data": tool_facts},
        ))
        return result


# ---------------------------------------------------------------------------
# 4. ORCHESTRATOR AGENT (planning / task decomposition + orchestrator-worker)
# ---------------------------------------------------------------------------
class OrchestratorAgent:
    """Top-level agent. Decomposes the user's query (planning pattern),
    dispatches it to the Router to decide which worker(s) are needed
    (orchestrator-worker pattern), collects subtask results via the
    message bus, and synthesises a single final answer for the user."""

    def __init__(self, rag: "RAGPipeline"):
        self.router = RouterAgent()
        self.support = SupportAgent(rag)
        self.inventory = InventoryAgent()

    def handle_query(self, query: str) -> Dict[str, Any]:
        bus = MessageBus()
        bus.send(AgentMessage(sender="user", receiver="orchestrator",
                               type="query", content=query))

        route = self.router.classify(bus, query)

        subtask_results: List[Dict[str, Any]] = []
        if route in ("support", "both"):
            subtask_results.append({"agent": "support", **self.support.handle(bus, query)})
        if route in ("inventory", "both"):
            subtask_results.append({"agent": "inventory", **self.inventory.handle(bus, query)})

        if len(subtask_results) == 1:
            final_answer = subtask_results[0]["answer"]
        else:
            # Planning/aggregation step: synthesise multiple worker outputs
            # into one coherent answer.
            combined = "\n\n".join(
                f"[{r['agent']} agent]: {r['answer']}" for r in subtask_results
            )
            system = (
                "Combine the following outputs from two internal agents into "
                "a single, coherent, non-repetitive answer for the user. "
                "Keep all factual content from both."
            )
            resp = call_llm("synthesis", system, combined, max_tokens=500)
            final_answer = resp.text or combined

        bus.send(AgentMessage(sender="orchestrator", receiver="user",
                               type="final_answer", content=final_answer))

        return {
            "route": route,
            "final_answer": final_answer,
            "subtask_results": subtask_results,
            "trace": bus.trace(),
        }
