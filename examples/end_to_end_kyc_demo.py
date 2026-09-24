from opentaf.agents.registry import AgentDefinition, AgentRegistry
from opentaf.audit.events import AuditLogger, InMemoryAuditRepository
from opentaf.data.customer_repository import CustomerRepository
from opentaf.governance.approval import ApprovalService
from opentaf.governance.policy import PolicyEngine
from opentaf.models.customer import Customer
from opentaf.orchestration.orchestrator import (
    OrchestrationRequest,
    Orchestrator,
)
from opentaf.tools.executor import InMemoryToolExecutor
from opentaf.tools.kyc import KYCValidationTool
from opentaf.tools.registry import ToolDefinition, ToolRegistry


# --------------------------------------------------
# 1. Synthetic Customer Data
# --------------------------------------------------

customer_repository = CustomerRepository()

customer_repository.save(
    Customer(
        customer_id="SYN-CUST-001",
        full_name="Aarav Mehta",
        date_of_birth="1990-04-15",
        document_id="SYN-DOC-001",
        document_verified=True,
        kyc_status="pending",
    )
)


# --------------------------------------------------
# 2. Real KYC Enterprise Tool
# --------------------------------------------------

kyc_tool = KYCValidationTool(
    customer_repository
)


# --------------------------------------------------
# 3. Tool Executor
# --------------------------------------------------

tool_executor = InMemoryToolExecutor()

tool_executor.register(
    "TOOL-KYC-VALIDATE",
    kyc_tool,
)


# --------------------------------------------------
# 4. Agent Registry
# --------------------------------------------------

agent_registry = AgentRegistry()

kyc_agent = AgentDefinition(
    agent_id="OTAF-KYC-001",
    name="KYC Validation Agent",
    purpose="Support customer KYC validation",
    owner="Customer Operations",
    risk_level="high",
    autonomy_level="L2",
)

agent_registry.register(kyc_agent)
agent_registry.approve(
    "OTAF-KYC-001"
)


# --------------------------------------------------
# 5. Tool Registry
# --------------------------------------------------

tool_registry = ToolRegistry()

kyc_tool_definition = ToolDefinition(
    tool_id="TOOL-KYC-VALIDATE",
    name="KYC Validation Tool",
    purpose="Validate synthetic customer KYC information",
    risk_level="high",
    allowed_agents=[
        "OTAF-KYC-001"
    ],
    requires_human_approval=True,
)

tool_registry.register(
    kyc_tool_definition
)


# --------------------------------------------------
# 6. Governance Services
# --------------------------------------------------

policy_engine = PolicyEngine()

approval_service = ApprovalService()

audit_repository = InMemoryAuditRepository()

audit_logger = AuditLogger(
    audit_repository
)


# --------------------------------------------------
# 7. Orchestrator
# --------------------------------------------------

orchestrator = Orchestrator(
    agent_registry=agent_registry,
    tool_registry=tool_registry,
    policy_engine=policy_engine,
    audit_logger=audit_logger,
    approval_service=approval_service,
    tool_executor=tool_executor,
)


# --------------------------------------------------
# 8. Submit KYC Request
# --------------------------------------------------

request = OrchestrationRequest(
    request_id="REQ-KYC-001",
    user_id="synthetic-user-001",
    agent_id="OTAF-KYC-001",
    tool_id="TOOL-KYC-VALIDATE",
    action="validate",
    context={
        "customer_id": "SYN-CUST-001",
    },
)


print("\n=== OpenTAF KYC Workflow ===\n")

result = orchestrator.process(
    request
)

print("Initial Request")
print("----------------")
print(f"Status: {result.status}")
print(f"Message: {result.message}")
print(f"Approval ID: {result.approval_id}")


# --------------------------------------------------
# 9. Human Approval
# --------------------------------------------------

if result.status == "pending_approval":

    print("\nHuman Approval")
    print("----------------")

    result = orchestrator.approve_and_execute(
        approval_id=result.approval_id,
        decided_by="synthetic-reviewer-001",
        decision_reason=(
            "Synthetic KYC request reviewed and approved."
        ),
    )

    print(f"Status: {result.status}")
    print(f"Message: {result.message}")


# --------------------------------------------------
# 10. Display KYC Result
# --------------------------------------------------

if result.execution_result is not None:

    print("\nKYC Validation Result")
    print("----------------------")

    kyc_result = result.execution_result

    print(f"Customer ID: {kyc_result.customer_id}")
    print(f"Status: {kyc_result.status}")
    print(
        f"Document Verified: "
        f"{kyc_result.document_verified}"
    )
    print(f"Risk Flag: {kyc_result.risk_flag}")
    print(f"Message: {kyc_result.message}")


# --------------------------------------------------
# 11. Audit Trail
# --------------------------------------------------

print("\nAudit Trail")
print("-----------")

for event in audit_logger.list_events():

    print(
        f"{event.event_id} | "
        f"{event.event_type} | "
        f"{event.decision} | "
        f"{event.outcome}"
    )
