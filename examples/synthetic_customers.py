from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer


repository = CustomerRepository()

repository.save(
    Customer(
        customer_id="SYN-CUST-001",
        full_name="Aarav Mehta",
        date_of_birth="1990-04-15",
        document_id="SYN-DOC-001",
        document_verified=True,
        kyc_status="pending",
        risk_flag=None,
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

for customer in repository.list_customers():
    print(
        f"{customer.customer_id} | "
        f"{customer.full_name} | "
        f"KYC: {customer.kyc_status} | "
        f"Document Verified: {customer.document_verified} | "
        f"Risk Flag: {customer.risk_flag}"
    )
