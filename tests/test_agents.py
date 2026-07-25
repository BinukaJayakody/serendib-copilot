import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.protocol import MessageBus
from src.agents.agents import RouterAgent, InventoryAgent, OrchestratorAgent
from src.models.clients import LLMResponse


def fake_response(text, provider="groq", model="llama-3.1-8b-instant"):
    return LLMResponse(text=text, provider=provider, model=model, latency_s=0.01)


@patch("src.agents.agents.call_llm")
def test_router_classifies_and_falls_back_on_unexpected_output(mock_call):
    mock_call.return_value = fake_response("support")
    bus = MessageBus()
    route = RouterAgent().classify(bus, "what are your shipping terms")
    assert route == "support"
    assert bus.trace()[-1]["type"] == "route_decision"


@patch("src.agents.agents.call_llm")
def test_router_falls_back_to_support_on_garbage_output(mock_call):
    mock_call.return_value = fake_response("I am not sure what to say")
    bus = MessageBus()
    route = RouterAgent().classify(bus, "random question")
    assert route == "support"  # default fallback, never crashes


@patch("src.agents.agents.call_llm")
def test_inventory_agent_reflection_runs_two_llm_calls(mock_call):
    # first call = draft, second call = reflection/critique
    mock_call.side_effect = [
        fake_response("Cardamom is low, reorder 50kg.", model="llama-3.3-70b-versatile"),
        fake_response("Cardamom is below reorder point (310kg < 400kg). "
                       "Recommend reordering at least the 100kg MOQ.",
                       model="llama-3.3-70b-versatile"),
    ]
    bus = MessageBus()
    result = InventoryAgent().handle(bus, "how much cardamom do we have")
    assert mock_call.call_count == 2
    assert "MOQ" in result["answer"]
    assert "draft_before_reflection" in result


@patch("src.agents.agents.call_llm")
def test_inventory_agent_unknown_product_skips_llm(mock_call):
    bus = MessageBus()
    result = InventoryAgent().handle(bus, "do we have saffron")
    mock_call.assert_not_called()
    assert "couldn't match" in result["answer"]


@patch("src.agents.agents.call_llm")
def test_orchestrator_routes_to_support_only(mock_call):
    mock_call.return_value = fake_response("support")
    fake_rag = MagicMock()
    fake_rag.retrieve.return_value = []

    with patch("src.agents.agents.call_llm") as mocked:
        mocked.side_effect = [
            fake_response("support"),  # router
            fake_response("Our MOQ for pepper is 1000kg.", model="anthropic/claude-3.5-haiku",
                           provider="openrouter"),  # support synthesis
        ]
        orchestrator = OrchestratorAgent(fake_rag)
        result = orchestrator.handle_query("what's the MOQ for pepper")

    assert result["route"] == "support"
    assert len(result["subtask_results"]) == 1
    assert result["subtask_results"][0]["agent"] == "support"
    assert any(m["type"] == "final_answer" for m in result["trace"])
