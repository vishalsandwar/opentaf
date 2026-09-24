"""
OpenTAF Orchestrator

Coordinates agents, enterprise tools, policy decisions,
human approval requirements and audit events.
"""

from dataclasses import dataclass
from typing import Dict, Optional

from opentaf.agents.registry import AgentRegistry
from opentaf.audit.events import AuditEvent, AuditLogger
from opentaf.governance.policy import PolicyEngine
from opentaf.tools.registry import ToolRegistry


@dataclass
class OrchestrationRequest:
    """Represents a business request submitted to OpenTAF."""

    request_id: str
    user_id: str
    agent_id: str
    tool_id: str
    action: str
    context: Dict[str, str]


@dataclass
class OrchestrationResult:
    """Result returned by the orchestrator."""

    request_id: str
    status: str
    message: str
    human_approval_required: bool = False
    execution_result: Optional[str] = None


class Orchestrator:
    """Coordinates governed agent execution."""

    def __init__(
        self,
        agent_registry: AgentRegistry,
        tool_registry: ToolRegistry,
        policy_engine: PolicyEngine,
        audit_logger: AuditLogger,
    ) -> None:
        self._agent_registry = agent_registry
        self._tool_registry = tool_registry
        self._policy_engine = policy_engine
        self._audit_logger = audit_logger

    def process(
        self,
        request: OrchestrationRequest,
    ) -> OrchestrationResult:
        """Process a governed orchestration request."""

        agent = self._agent_registry.get(request.agent_id)

        if agent is None:
            return OrchestrationResult(
                request_id=request.request_id,
                status="rejected",
                message="Agent not found.",
            )

        tool = self._tool_registry.get(request.tool_id)

        if tool is None:
            return OrchestrationResult(
                request_id=request.request_id,
                status="rejected",
                message="Tool not found.",
            )

        decision = self._policy_engine.evaluate(
            agent,
            tool,
        )

        self._audit_logger.record(
            AuditEvent(
                event_id=f"{request.request_id}-POLICY",
                event_type="POLICY_DECISION",
                agent_id=agent.agent_id,
                user_id=request.user_id,
                tool_id=tool.tool_id,
                action=request.action,
                decision=(
                    "allowed"
                    if decision.allowed
                    else "denied"
                ),
                outcome=decision.reason,
                details={
                    "request_id": request.request_id,
                    "risk_level": tool.risk_level,
                    "autonomy_level": agent.autonomy_level,
                },
            )
        )

        if not decision.allowed:
            return OrchestrationResult(
                request_id=request.request_id,
                status="rejected",
                message=decision.reason,
            )

        if decision.requires_human_approval:
            return OrchestrationResult(
                request_id=request.request_id,
                status="pending_approval",
                message=decision.reason,
                human_approval_required=True,
            )

        execution_result = (
            f"Tool {tool.tool_id} executed successfully."
        )

        self._audit_logger.record(
            AuditEvent(
                event_id=f"{request.request_id}-EXECUTION",
                event_type="TOOL_EXECUTION",
                agent_id=agent.agent_id,
                user_id=request.user_id,
                tool_id=tool.tool_id,
                action=request.action,
                decision="approved",
                outcome="executed",
                details={
                    "request_id": request.request_id,
                },
            )
        )

        return OrchestrationResult(
            request_id=request.request_id,
            status="completed",
            message="Request completed successfully.",
            execution_result=execution_result,
        )
