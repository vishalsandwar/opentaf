"""
OpenTAF Multi-Agent Workflow

Coordinates specialized agents through a shared
execution context.
"""

from dataclasses import dataclass
from typing import List

from opentaf.agents.base import Agent
from opentaf.agents.context import AgentExecutionContext


@dataclass
class AgentWorkflowResult:
    """Result of a multi-agent workflow."""

    request_id: str
    status: str
    completed_agents: List[str]
    results: dict[str, str]


class AgentWorkflow:
    """Executes a sequence of specialized agents."""

    def __init__(
        self,
        agents: List[Agent],
    ) -> None:
        self._agents = agents

    def execute(
        self,
        context: AgentExecutionContext,
    ) -> AgentWorkflowResult:
        """Execute all agents in sequence."""

        completed_agents: List[str] = []

        for agent in self._agents:
            agent.execute(context)

            completed_agents.append(
                agent.agent_id
            )

        return AgentWorkflowResult(
            request_id=context.request_id,
            status="completed",
            completed_agents=completed_agents,
            results=dict(context.results),
        )
