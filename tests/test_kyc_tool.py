from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer
from opentaf.tools.kyc import KYCValidationTool


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


def test_verified_customer_passes_kyc():
    repository = create_repository()

    tool = KYCValidationTool(repository)

    result = tool.validate("SYN-CUST-001")

    assert result.status == "verified"
    assert result.document_verified is True
    assert result.message == (
        "Customer KYC successfully verified."
    )


def test_unverified_customer_requires_review():
    repository = create_repository()

    tool = KYCValidationTool(repository)

    result = tool.validate("SYN-CUST-002")

    assert result.status == "review_required"
    assert result.document_verified is False
    assert result.risk_flag == (
        "document_verification_required"
    )


def test_unknown_customer_is_not_found():
    repository = create_repository()

    tool = KYCValidationTool(repository)

    result = tool.validate("SYN-CUST-999")

    assert result.status == "not_found"
    assert result.document_verified is False
