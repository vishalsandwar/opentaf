from opentaf.agents.registry import AgentDefinition, AgentRegistry
from opentaf.audit.events import AuditLogger, InMemoryAuditRepository
from opentaf.governance.policy import PolicyEngine
from opentaf.orchestration.orchestrator import (
    OrchestrationRequest,
    Orchestrator,
)
from opentaf.tools.registry import ToolDefinition, ToolRegistry


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

    orchestrator = Orchestrator(
        agent_registry=agent_registry,
        tool_registry=tool_registry,
        policy_engine=PolicyEngine(),
        audit_logger=audit_logger,
    )

    return orchestrator, audit_logger


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


def test_request_is_pending_when_human_approval_is_required():
    orchestrator, audit = create_orchestrator(
        tool_requires_approval=True,
    )

    result = orchestrator.process(create_request())

    assert result.status == "pending_approval"
    assert result.human_approval_required is True

    events = audit.list_events()

    assert len(events) == 1
    assert events[0].event_type == "POLICY_DECISION"
    assert events[0].decision == "allowed"


def test_unauthorised_agent_request_is_rejected():
    orchestrator, audit = create_orchestrator(
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
    orchestrator, audit = create_orchestrator(
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


def test_request_executes_when_approval_is_not_required():
    orchestrator, audit = create_orchestrator(
        autonomy_level="L2",
        tool_requires_approval=False,
    )

    result = orchestrator.process(create_request())

    assert result.status == "completed"
    assert result.execution_result == (
        "Tool TOOL-KYC-VALIDATE executed successfully."
    )

    events = audit.list_events()

    assert len(events) == 2

    assert events[0].event_type == "POLICY_DECISION"
    assert events[1].event_type == "TOOL_EXECUTION"
    assert events[1].outcome == "executed"
