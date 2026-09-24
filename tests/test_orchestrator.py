from opentaf.agents.registry import AgentDefinition, AgentRegistry
from opentaf.audit.events import AuditLogger, InMemoryAuditRepository
from opentaf.governance.approval import ApprovalService
from opentaf.governance.policy import PolicyEngine
from opentaf.orchestration.orchestrator import (
    OrchestrationRequest,
    Orchestrator,
)
from opentaf.tools.executor import InMemoryToolExecutor
from opentaf.tools.registry import ToolDefinition, ToolRegistry



class SyntheticKYCExecutor:
    def validate_kyc(self, customer_id):
        return f"KYC validation completed for {customer_id}"


def create_orchestrator(
    autonomy_level="L2",
    tool_requires_approval=True,
    tool_allowed_agents=None,
    approve_agent=True,
):
    agent_registry = AgentRegistry()
    tool_registry = ToolRegistry()

    agent = AgentDefinition(
        agent_id="OTAF-KYC-001",
        name="KYC Validation Agent",
        purpose="Support customer KYC validation",
        owner="Customer Operations",
        risk_level="high",
        autonomy_level=autonomy_level,
    )

    agent_registry.register(agent)

    if approve_agent:
        agent_registry.approve(agent.agent_id)

    if tool_allowed_agents is None:
        tool_allowed_agents = ["OTAF-KYC-001"]

    tool = ToolDefinition(
        tool_id="TOOL-KYC-VALIDATE",
        name="KYC Validation Tool",
        purpose="Validate synthetic customer KYC information",
        risk_level="high",
        allowed_agents=tool_allowed_agents,
        requires_human_approval=tool_requires_approval,
    )

    tool_registry.register(tool)

    repository = InMemoryAuditRepository()
    audit_logger = AuditLogger(repository)

    approval_service = ApprovalService()
    tool_executor = InMemoryToolExecutor()

    tool_executor.register(
        "TOOL-KYC-VALIDATE",
        SyntheticKYCExecutor(),
    )

    orchestrator = Orchestrator(
        agent_registry=agent_registry,
        tool_registry=tool_registry,
        policy_engine=PolicyEngine(),
        audit_logger=audit_logger,
        approval_service=approval_service,
        tool_executor=tool_executor,
    )

    return orchestrator, audit_logger, approval_service


def create_request():
    return OrchestrationRequest(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        agent_id="OTAF-KYC-001",
        tool_id="TOOL-KYC-VALIDATE",
        action="validate_kyc",
        context={
            "customer_id": "SYN-CUST-001",
        },
    )


def test_request_creates_human_approval():
    orchestrator, audit, approval_service = create_orchestrator(
        tool_requires_approval=True,
    )

    result = orchestrator.process(create_request())

    assert result.status == "pending_approval"
    assert result.human_approval_required is True
    assert result.approval_id == "APR-REQ-001"

    approval = approval_service.get("APR-REQ-001")

    assert approval is not None
    assert approval.status == "pending"

    events = audit.list_events()

    assert len(events) == 2
    assert events[0].event_type == "POLICY_DECISION"
    assert events[1].event_type == "HUMAN_APPROVAL_REQUEST"


def test_approval_executes_request():
    orchestrator, audit, approval_service = create_orchestrator(
        tool_requires_approval=True,
    )

    result = orchestrator.process(create_request())

    assert result.status == "pending_approval"

    result = orchestrator.approve_and_execute(
        approval_id=result.approval_id,
        decided_by="synthetic-reviewer-001",
        decision_reason="KYC information reviewed and approved.",
    )

    assert result.status == "completed"

    approval = approval_service.get("APR-REQ-001")

    assert approval.status == "approved"

    events = audit.list_events()

    assert len(events) == 4
    assert events[2].event_type == "HUMAN_APPROVAL"
    assert events[2].decision == "approved"
    assert events[3].event_type == "TOOL_EXECUTION"


def test_rejected_approval_blocks_execution():
    orchestrator, audit, approval_service = create_orchestrator(
        tool_requires_approval=True,
    )

    result = orchestrator.process(create_request())

    assert result.status == "pending_approval"

    result = orchestrator.reject_approval(
        approval_id=result.approval_id,
        decided_by="synthetic-reviewer-001",
        decision_reason="KYC information requires correction.",
    )

    assert result.status == "rejected"

    approval = approval_service.get("APR-REQ-001")

    assert approval.status == "rejected"

    events = audit.list_events()

    assert len(events) == 3
    assert events[2].event_type == "HUMAN_APPROVAL"
    assert events[2].decision == "rejected"


def test_unauthorised_agent_request_is_rejected():
    orchestrator, audit, _ = create_orchestrator(
        tool_requires_approval=False,
        tool_allowed_agents=["OTAF-DOCUMENT-001"],
    )

    result = orchestrator.process(create_request())

    assert result.status == "rejected"
    assert result.message == (
        "Agent is not authorised to use this tool."
    )

    events = audit.list_events()

    assert len(events) == 1
    assert events[0].decision == "denied"


def test_unapproved_agent_request_is_rejected():
    orchestrator, audit, _ = create_orchestrator(
        tool_requires_approval=False,
        approve_agent=False,
    )

    result = orchestrator.process(create_request())

    assert result.status == "rejected"
    assert result.message == (
        "Agent is not approved for execution."
    )

    events = audit.list_events()

    assert len(events) == 1
    assert events[0].decision == "denied"


def test_request_executes_without_human_approval():
    orchestrator, audit, _ = create_orchestrator(
        autonomy_level="L2",
        tool_requires_approval=False,
    )

    result = orchestrator.process(create_request())

    assert result.status == "completed"
    assert result.execution_result == (
        "KYC validation completed for SYN-CUST-001"
    )

    events = audit.list_events()

    assert len(events) == 2

    assert events[0].event_type == "POLICY_DECISION"
    assert events[1].event_type == "TOOL_EXECUTION"
