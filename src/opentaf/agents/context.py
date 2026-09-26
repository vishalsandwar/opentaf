"""
OpenTAF Agent Execution Context

Provides a controlled shared context for multi-agent workflows.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AgentExecutionContext:
    """Shared context passed through a multi-agent workflow."""

    request_id: str
    user_id: str
    objective: str
    data: Dict[str, str] = field(default_factory=dict)
    results: Dict[str, str] = field(default_factory=dict)

    def add_result(
        self,
        agent_id: str,
        result: str,
    ) -> None:
        """Store an agent result in the execution context."""

        self.results[agent_id] = result

    def get_result(
        self,
        agent_id: str,
    ) -> str | None:
        """Retrieve a result produced by an agent."""

        return self.results.get(agent_id)
