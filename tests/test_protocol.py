import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.agents.protocol import AgentMessage, MessageBus


def test_message_has_unique_id_and_timestamp():
    m1 = AgentMessage(sender="a", receiver="b", type="query", content="hi")
    m2 = AgentMessage(sender="a", receiver="b", type="query", content="hi")
    assert m1.message_id != m2.message_id


def test_bus_records_messages_in_order():
    bus = MessageBus()
    bus.send(AgentMessage(sender="user", receiver="orchestrator", type="query", content="q1"))
    bus.send(AgentMessage(sender="orchestrator", receiver="router", type="classify", content="q1"))
    trace = bus.trace()
    assert len(trace) == 2
    assert trace[0]["sender"] == "user"
    assert trace[1]["sender"] == "orchestrator"


def test_bus_reset_clears_log():
    bus = MessageBus()
    bus.send(AgentMessage(sender="user", receiver="orchestrator", type="query", content="q1"))
    bus.reset()
    assert bus.trace() == []


def test_to_dict_round_trip_fields():
    m = AgentMessage(sender="router", receiver="orchestrator", type="route_decision",
                      content="support", context={"model": "llama-3.1-8b-instant"})
    d = m.to_dict()
    assert d["sender"] == "router"
    assert d["context"]["model"] == "llama-3.1-8b-instant"
