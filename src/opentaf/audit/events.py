"""
OpenTAF Audit & Event Framework

Provides a lightweight audit mechanism for recording
agent, tool, policy, approval and execution events.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass
class AuditEvent:
    """Represents a traceable OpenTAF event."""

    event_type: str
    agent_id: str
    event_id: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    user_id: Optional[str] = None
    tool_id: Optional[str] = None
    action: Optional[str] = None
    decision: Optional[str] = None
    outcome: Optional[str] = None
    details: Dict[str, str] = field(default_factory=dict)


class AuditLogger:
    """In-memory audit logger for the OpenTAF reference implementation."""

    def __init__(self) -> None:
        self._events: List[AuditEvent] = []

    def record(self, event: AuditEvent) -> None:
        """Record an audit event."""

        self._events.append(event)

    def list_events(self) -> List[AuditEvent]:
        """Return all recorded events."""

        return list(self._events)

    def find_by_agent(
        self,
        agent_id: str,
    ) -> List[AuditEvent]:
        """Return events associated with an agent."""

        return [
            event
            for event in self._events
            if event.agent_id == agent_id
        ]

    def find_by_event_type(
        self,
        event_type: str,
    ) -> List[AuditEvent]:
        """Return events of a specific type."""

        return [
            event
            for event in self._events
            if event.event_type == event_type
        ]
