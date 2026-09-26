from opentaf.agents.context import AgentExecutionContext
from opentaf.agents.risk import RiskAgent
from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer


def create_repository():
    repository = CustomerRepository()

    repository.save(
        Customer(
            customer_id="SYN-CUST-001",
            full_name="Aarav Mehta",
            date_of_birth="1990-04-15",
            document_id="SYN-DOC-001",
            document_verified=True,
            kyc_status="pending",
        )
    )

    repository.save(
        Customer(
            customer_id="SYN-CUST-002",
            full_name="Priya Sharma",
            date_of_birth="1987-09-21",
            document_id="SYN-DOC-002",
            document_verified=False,
            kyc_status="pending",
            risk_flag="document_verification_required",
        )
    )

    return repository


def create_context(customer_id):
    return AgentExecutionContext(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
        data={
            "customer_id": customer_id,
        },
    )


def test_low_risk_customer_is_identified():
    repository = create_repository()

    agent = RiskAgent(repository)

    context = create_context(
        "SYN-CUST-001"
    )

    context.add_result(
        "OTAF-DOCUMENT-001",
        "documents_verified",
    )

    result = agent.execute(context)

    assert result == "low_risk"

    assert (
        context.get_result(
            "OTAF-RISK-001"
        )
        == "low_risk"
    )


def test_document_issue_requires_review():
    repository = create_repository()

    agent = RiskAgent(repository)

    context = create_context(
        "SYN-CUST-002"
    )

    context.add_result(
        "OTAF-DOCUMENT-001",
        "document_verification_required",
    )

    result = agent.execute(context)

    assert result == "review_required"


def test_risk_flag_is_detected():
    repository = create_repository()

    repository.save(
        Customer(
            customer_id="SYN-CUST-003",
            full_name="Rahul Verma",
            date_of_birth="1985-02-11",
            document_id="SYN-DOC-003",
            document_verified=True,
            kyc_status="pending",
            risk_flag="manual_risk_review",
        )
    )

    agent = RiskAgent(repository)

    context = create_context(
        "SYN-CUST-003"
    )

    context.add_result(
        "OTAF-DOCUMENT-001",
        "documents_verified",
    )

    result = agent.execute(context)

    assert result == "risk_flagged"


def test_missing_document_assessment_is_detected():
    repository = create_repository()

    agent = RiskAgent(repository)

    context = create_context(
        "SYN-CUST-001"
    )

    result = agent.execute(context)

    assert result == "document_assessment_missing"


def test_missing_customer_id_is_detected():
    repository = create_repository()

    agent = RiskAgent(repository)

    context = AgentExecutionContext(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
    )

    result = agent.execute(context)

    assert result == "customer_id_missing"
