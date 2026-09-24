
"""
OpenTAF Policy Engine

Evaluates whether an agent is permitted to invoke a
registered enterprise tool.
"""

from dataclasses import dataclass

from opentaf.agents.registry import AgentDefinition
from opentaf.tools.registry import ToolDefinition


@dataclass
class PolicyDecision:
    """Result of a policy evaluation."""

    allowed: bool
    reason: str
    requires_human_approval: bool = False


class PolicyEngine:
    """Evaluates agent-to-tool access."""

    def evaluate(
        self,
        agent: AgentDefinition,
        tool: ToolDefinition,
    ) -> PolicyDecision:
        """Evaluate whether an agent may invoke a tool."""

        if agent.status != "approved":
            return PolicyDecision(
                allowed=False,
                reason="Agent is not approved for execution."
            )

        if tool.status != "active":
            return PolicyDecision(
                allowed=False,
                reason="Tool is not active."
            )

        if agent.agent_id not in tool.allowed_agents:
            return PolicyDecision(
                allowed=False,
                reason="Agent is not authorised to use this tool."
            )

        if (
            tool.risk_level == "high"
            and agent.autonomy_level != "L2"
        ):
            return PolicyDecision(
                allowed=False,
                reason=(
                    "High-risk tool requires an appropriate "
                    "human-approved autonomy level."
                )
            )

        if tool.requires_human_approval:
            return PolicyDecision(
                allowed=True,
                reason="Tool is authorised but requires human approval.",
                requires_human_approval=True,
            )

        return PolicyDecision(
            allowed=True,
            reason="Agent is authorised to use the tool."
        )
