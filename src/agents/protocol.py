"""
Custom agent-to-agent communication protocol.

Inspired by the shape of MCP/A2A messages (a typed envelope carrying a
role, a task, structured context, and a result) but implemented directly
in Python dataclasses rather than pulling in LangGraph/CrewAI/AutoGen, so
that every hop in the conversation is visible and inspectable in the
Streamlit UI's "agent trace" panel.

Message flow for a single user turn:

    User
      -> AgentMessage(sender="user", receiver="orchestrator", type="query")
    Orchestrator
      -> AgentMessage(sender="orchestrator", receiver="router", type="classify")
    Router
      -> AgentMessage(sender="router", receiver="orchestrator", type="route_decision")
    Orchestrator
      -> AgentMessage(sender="orchestrator", receiver="support"|"inventory", type="subtask")
    Support/Inventory
      -> AgentMessage(sender="support"|"inventory", receiver="orchestrator", type="subtask_result")
    Orchestrator
      -> AgentMessage(sender="orchestrator", receiver="user", type="final_answer")

See README.md for the corresponding sequence diagram.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AgentMessage:
    sender: str
    receiver: str
    type: str                     # e.g. "query", "classify", "route_decision",
                                   # "subtask", "subtask_result", "final_answer"
    content: str                  # human-readable payload
    context: Dict[str, Any] = field(default_factory=dict)  # structured data
    message_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    timestamp: float = field(default_factory=time.time)
    parent_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "message_id": self.message_id,
            "parent_id": self.parent_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.type,
            "content": self.content,
            "context": self.context,
            "timestamp": self.timestamp,
        }


class MessageBus:
    """Records every AgentMessage exchanged during a turn, so the UI can
    render a full agent-to-agent trace for transparency/demo purposes."""

    def __init__(self) -> None:
        self.log: list[AgentMessage] = []

    def send(self, msg: AgentMessage) -> AgentMessage:
        self.log.append(msg)
        return msg

    def trace(self) -> list[Dict[str, Any]]:
        return [m.to_dict() for m in self.log]

    def reset(self) -> None:
        self.log = []
