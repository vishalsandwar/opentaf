from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer
from opentaf.tools.kyc import KYCValidationTool


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


tool = KYCValidationTool(repository)


for customer_id in [
    "SYN-CUST-001",
    "SYN-CUST-002",
]:
    result = tool.validate(customer_id)

    print(
        f"{result.customer_id} | "
        f"Status: {result.status} | "
        f"Document Verified: {result.document_verified} | "
        f"Risk: {result.risk_flag} | "
        f"{result.message}"
    )
