from opentaf.agents.context import AgentExecutionContext
from opentaf.agents.document import DocumentAgent
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


def test_verified_documents_are_detected():
    repository = create_repository()

    agent = DocumentAgent(repository)

    context = create_context(
        "SYN-CUST-001"
    )

    result = agent.execute(context)

    assert result == "documents_verified"

    assert (
        context.get_result(
            "OTAF-DOCUMENT-001"
        )
        == "documents_verified"
    )


def test_unverified_documents_require_review():
    repository = create_repository()

    agent = DocumentAgent(repository)

    context = create_context(
        "SYN-CUST-002"
    )

    result = agent.execute(context)

    assert result == (
        "document_verification_required"
    )


def test_unknown_customer_is_detected():
    repository = create_repository()

    agent = DocumentAgent(repository)

    context = create_context(
        "SYN-CUST-999"
    )

    result = agent.execute(context)

    assert result == "customer_not_found"


def test_missing_customer_id_is_detected():
    repository = create_repository()

    agent = DocumentAgent(repository)

    context = AgentExecutionContext(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
    )

    result = agent.execute(context)

    assert result == "customer_id_missing"
