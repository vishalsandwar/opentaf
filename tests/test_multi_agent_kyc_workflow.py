from opentaf.agents.compliance import ComplianceAgent
from opentaf.agents.context import AgentExecutionContext
from opentaf.agents.document import DocumentAgent
from opentaf.agents.risk import RiskAgent
from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer
from opentaf.orchestration.agent_workflow import AgentWorkflow


def create_repository():
    repository = CustomerRepository()

    repository.save(
        Customer(
            customer_id="SYN-CUST-001",
            full_name="Aarav Mehta",
            date_of_birth="1990-01-15",
            document_id="DOC-SYN-001",
            document_verified=True,
            kyc_status="pending",
        )
    )

    return repository


def create_context():
    return AgentExecutionContext(
        request_id="REQ-KYC-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
        data={
            "customer_id": "SYN-CUST-001",
        },
    )


def test_multi_agent_kyc_workflow_completes_successfully():
    repository = create_repository()

    workflow = AgentWorkflow(
        [
            DocumentAgent(repository),
            RiskAgent(repository),
            ComplianceAgent(),
        ]
    )

    result = workflow.execute(
        create_context()
    )

    assert result.status == "completed"

    assert result.results[
        "OTAF-DOCUMENT-001"
    ] == "documents_verified"

    assert result.results[
        "OTAF-RISK-001"
    ] == "low_risk"

    assert result.results[
        "OTAF-COMPLIANCE-001"
    ] == "compliance_clear"


def test_multi_agent_workflow_preserves_execution_order():
    repository = create_repository()

    workflow = AgentWorkflow(
        [
            DocumentAgent(repository),
            RiskAgent(repository),
            ComplianceAgent(),
        ]
    )

    result = workflow.execute(
        create_context()
    )

    assert result.completed_agents == [
        "OTAF-DOCUMENT-001",
        "OTAF-RISK-001",
        "OTAF-COMPLIANCE-001",
    ]
