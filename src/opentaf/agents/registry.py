"""
OpenTAF Agent Registry

Maintains the authoritative inventory of agents within the
OpenTAF reference implementation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class AgentDefinition:
    """Definition of an OpenTAF agent."""

    agent_id: str
    name: str
    purpose: str
    owner: str
    risk_level: str
    autonomy_level: str
    tools: List[str] = field(default_factory=list)
    status: str = "draft"


class AgentRegistry:
    """Registry for managing OpenTAF agents."""

    def __init__(self) -> None:
        self._agents: Dict[str, AgentDefinition] = {}

    def register(self, agent: AgentDefinition) -> None:
        """Register a new agent."""

        if agent.agent_id in self._agents:
            raise ValueError(
                f"Agent already registered: {agent.agent_id}"
            )

        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Optional[AgentDefinition]:
        """Retrieve an agent by ID."""

        return self._agents.get(agent_id)

    def list_agents(self) -> List[AgentDefinition]:
        """Return all registered agents."""

        return list(self._agents.values())

    def approve(self, agent_id: str) -> None:
        """Mark an agent as approved."""

        agent = self.get(agent_id)

        if agent is None:
            raise ValueError(
                f"Agent not found: {agent_id}"
            )

        agent.status = "approved"

    def retire(self, agent_id: str) -> None:
        """Retire an agent."""

        agent = self.get(agent_id)

        if agent is None:
            raise ValueError(
                f"Agent not found: {agent_id}"
            )

        agent.status = "retired"
