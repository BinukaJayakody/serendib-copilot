"""
Serendib Spice & Tea Traders — Agentic AI Co-Pilot
Streamlit entrypoint. Deploy target: Streamlit Community Cloud.

Secrets (GROQ_API_KEY, OPENROUTER_API_KEY) are read from environment
variables, which Streamlit Cloud populates from st.secrets automatically
when the app is deployed with a [secrets] TOML configured in the dashboard.
Locally, use a .env file (never committed — see .gitignore) or export the
variables in your shell.
"""

import os
import sys
import time

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from src.agents.agents import OrchestratorAgent  # noqa: E402
from src.rag.pipeline import RAGPipeline  # noqa: E402

# ---- Streamlit -> environment variable bridge for secrets ----
for key in ("GROQ_API_KEY", "OPENROUTER_API_KEY"):
    if key in st.secrets and not os.environ.get(key):
        os.environ[key] = st.secrets[key]

st.set_page_config(page_title="Serendib Spice & Tea Co-Pilot", layout="wide")


@st.cache_resource(show_spinner="Building knowledge base index (first run only)...")
def get_orchestrator() -> OrchestratorAgent:
    kb_dir = os.path.join(os.path.dirname(__file__), "data", "knowledge_base")
    rag = RAGPipeline(kb_dir=kb_dir)
    rag.ensure_ready()
    return OrchestratorAgent(rag)


def render_trace(trace: list[dict]) -> None:
    for m in trace:
        with st.container(border=True):
            st.markdown(f"**{m['sender']} → {m['receiver']}**  `{m['type']}`")
            st.caption(m["content"][:400] + ("..." if len(m["content"]) > 400 else ""))
            if m.get("context"):
                st.json(m["context"], expanded=False)


def main() -> None:
    st.title(" Serendib Spice & Tea Traders — Agentic Co-Pilot")
    st.caption(
        "An internal assistant for a Sri Lankan spice & tea export SME. "
        "Ask about products, policies, shipping, or stock levels."
    )

    missing = [k for k in ("GROQ_API_KEY", "OPENROUTER_API_KEY") if not os.environ.get(k)]
    if missing:
        st.warning(
            f"Missing API key(s): {', '.join(missing)}. Set them in Streamlit "
            "secrets (Settings → Secrets) or as environment variables to get "
            "live model responses. The app will still run but agent replies "
            "will show an error instead of an answer."
        )

    with st.sidebar:
        st.header("About this system")
        st.markdown(
            "- **Orchestrator** decomposes each query and dispatches it\n"
            "- **Router** (Groq Llama 3.1 8B) classifies intent\n"
            "- **Support agent** (ReAct + RAG, OpenRouter Claude 3.5 Haiku) "
            "answers product/policy questions grounded in company documents\n"
            "- **Inventory agent** (Groq Llama 3.3 70B, tool-use + reflection) "
            "answers stock questions and drafts reorder recommendations\n"
        )
        
    examples = [
        "What's your MOQ for cardamom and is it in stock?",
        "Do you ship to the EU and what documents come with the shipment?",
        "Is vanilla below reorder point? What should we order?",
        "What are your payment terms for a new buyer, and how much black pepper do we have on hand?",
    ]
    query = st.text_input("Ask the co-pilot:", placeholder=examples[0])
    cols = st.columns(len(examples))
    for c, ex in zip(cols, examples):
        if c.button(ex, use_container_width=True):
            query = ex

    if st.button("Ask", type="primary") and query:
        orchestrator = get_orchestrator()
        t0 = time.time()
        with st.spinner("Agents working..."):
            result = orchestrator.handle_query(query)
        elapsed = time.time() - t0

        st.subheader("Answer")
        st.write(result["final_answer"])
        st.caption(f"Route: `{result['route']}` · total time: {elapsed:.2f}s")

        for r in result["subtask_results"]:
            if r.get("sources"):
                st.caption(f"Grounded in: {', '.join(r['sources'])}")
            if r.get("error"):
                st.error(f"{r['agent']} agent error: {r['error']}")

        with st.expander(" Agent-to-agent trace (for demo/marking purposes)"):
            render_trace(result["trace"])

        with st.expander(" Reflection detail (inventory agent, if used)"):
            for r in result["subtask_results"]:
                if r.get("agent") == "inventory" and "draft_before_reflection" in r:
                    st.markdown("**Draft (before self-critique):**")
                    st.code(r["draft_before_reflection"])
                    st.markdown("**Tool data used:**")
                    st.code(r["tool_data"])
                    st.markdown("**Final (after reflection):**")
                    st.code(r["answer"])


if __name__ == "__main__":
    main()
