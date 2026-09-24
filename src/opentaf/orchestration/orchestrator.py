"""
OpenTAF Orchestrator

Coordinates agents, enterprise tools, policy decisions,
human approvals, tool execution and audit events.
"""

from dataclasses import dataclass
from typing import Dict, Optional

from opentaf.agents.registry import AgentRegistry
from opentaf.audit.events import AuditEvent, AuditLogger
from opentaf.governance.approval import ApprovalService
from opentaf.governance.policy import PolicyEngine
from opentaf.tools.executor import ToolExecutor
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
    approval_id: Optional[str] = None
    execution_result: Optional[object] = None


class Orchestrator:
    """Coordinates governed agent execution."""

    def __init__(
        self,
        agent_registry: AgentRegistry,
        tool_registry: ToolRegistry,
        policy_engine: PolicyEngine,
        audit_logger: AuditLogger,
        approval_service: ApprovalService,
        tool_executor: ToolExecutor,
    ) -> None:
        self._agent_registry = agent_registry
        self._tool_registry = tool_registry
        self._policy_engine = policy_engine
        self._audit_logger = audit_logger
        self._approval_service = approval_service
        self._tool_executor = tool_executor

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
            approval_id = f"APR-{request.request_id}"

            approval = self._approval_service.create_request(
                approval_id=approval_id,
                request_id=request.request_id,
                agent_id=agent.agent_id,
                tool_id=tool.tool_id,
                action=request.action,
                requested_by=request.user_id,
                reason=decision.reason,
                context=request.context,
            )

            self._audit_logger.record(
                AuditEvent(
                    event_id=f"{request.request_id}-APPROVAL",
                    event_type="HUMAN_APPROVAL_REQUEST",
                    agent_id=agent.agent_id,
                    user_id=request.user_id,
                    tool_id=tool.tool_id,
                    action=request.action,
                    decision="pending",
                    outcome="awaiting_human_approval",
                    details={
                        "approval_id": approval.approval_id,
                    },
                )
            )

            return OrchestrationResult(
                request_id=request.request_id,
                status="pending_approval",
                message="Human approval is required.",
                human_approval_required=True,
                approval_id=approval.approval_id,
            )

        return self._execute(
            request=request,
            agent_id=agent.agent_id,
            tool_id=tool.tool_id,
        )

    def approve_and_execute(
        self,
        approval_id: str,
        decided_by: str,
        decision_reason: str,
    ) -> OrchestrationResult:
        """Approve a pending request and execute the tool."""

        approval = self._approval_service.approve(
            approval_id=approval_id,
            decided_by=decided_by,
            decision_reason=decision_reason,
        )

        self._audit_logger.record(
            AuditEvent(
                event_id=f"{approval.request_id}-APPROVED",
                event_type="HUMAN_APPROVAL",
                agent_id=approval.agent_id,
                user_id=approval.requested_by,
                tool_id=approval.tool_id,
                action=approval.action,
                decision="approved",
                outcome="approved_for_execution",
                details={
                    "approval_id": approval.approval_id,
                    "decided_by": decided_by,
                },
            )
        )

        request = OrchestrationRequest(
            request_id=approval.request_id,
            user_id=approval.requested_by,
            agent_id=approval.agent_id,
            tool_id=approval.tool_id,
            action=approval.action,
            context=approval.context,
        )

        return self._execute(
            request=request,
            agent_id=approval.agent_id,
            tool_id=approval.tool_id,
        )

    def reject_approval(
        self,
        approval_id: str,
        decided_by: str,
        decision_reason: str,
    ) -> OrchestrationResult:
        """Reject a pending request."""

        approval = self._approval_service.reject(
            approval_id=approval_id,
            decided_by=decided_by,
            decision_reason=decision_reason,
        )

        self._audit_logger.record(
            AuditEvent(
                event_id=f"{approval.request_id}-REJECTED",
                event_type="HUMAN_APPROVAL",
                agent_id=approval.agent_id,
                user_id=approval.requested_by,
                tool_id=approval.tool_id,
                action=approval.action,
                decision="rejected",
                outcome="execution_blocked",
                details={
                    "approval_id": approval.approval_id,
                    "decided_by": decided_by,
                },
            )
        )

        return OrchestrationResult(
            request_id=approval.request_id,
            status="rejected",
            message="Human approval was rejected.",
        )

    def _execute(
        self,
        request: OrchestrationRequest,
        agent_id: str,
        tool_id: str,
    ) -> OrchestrationResult:
        """Execute an authorised enterprise tool."""

        try:
            execution_result = self._tool_executor.execute(
                tool_id=tool_id,
                action=request.action,
                parameters=request.context,
            )

        except Exception as exc:
            self._audit_logger.record(
                AuditEvent(
                    event_id=f"{request.request_id}-EXECUTION-FAILED",
                    event_type="TOOL_EXECUTION",
                    agent_id=agent_id,
                    user_id=request.user_id,
                    tool_id=tool_id,
                    action=request.action,
                    decision="approved",
                    outcome="execution_failed",
                    details={
                        "request_id": request.request_id,
                        "error": str(exc),
                    },
                )
            )

            return OrchestrationResult(
                request_id=request.request_id,
                status="execution_failed",
                message="Tool execution failed.",
            )

        self._audit_logger.record(
            AuditEvent(
                event_id=f"{request.request_id}-EXECUTION",
                event_type="TOOL_EXECUTION",
                agent_id=agent_id,
                user_id=request.user_id,
                tool_id=tool_id,
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
