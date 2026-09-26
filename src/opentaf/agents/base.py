"""
OpenTAF Agent Interface

Defines the common contract implemented by all
OpenTAF agents.
"""

from abc import ABC, abstractmethod

from opentaf.agents.context import AgentExecutionContext


class Agent(ABC):
    """Abstract contract for an OpenTAF agent."""

    @property
    @abstractmethod
    def agent_id(self) -> str:
        """Return the unique agent identifier."""

    @abstractmethod
    def execute(
        self,
        context: AgentExecutionContext,
    ) -> str:
        """Execute the agent against the workflow context."""
