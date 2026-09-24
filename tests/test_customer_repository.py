from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer


def create_customer():
    return Customer(
        customer_id="SYN-CUST-001",
        full_name="Aarav Mehta",
        date_of_birth="1990-04-15",
        document_id="SYN-DOC-001",
        document_verified=True,
        kyc_status="pending",
    )


def test_customer_can_be_saved_and_retrieved():
    repository = CustomerRepository()

    customer = create_customer()

    repository.save(customer)

    result = repository.get("SYN-CUST-001")

    assert result is not None
    assert result.full_name == "Aarav Mehta"


def test_unknown_customer_returns_none():
    repository = CustomerRepository()

    result = repository.get("SYN-CUST-999")

    assert result is None


def test_repository_can_list_customers():
    repository = CustomerRepository()

    repository.save(create_customer())

    customers = repository.list_customers()

    assert len(customers) == 1
    assert customers[0].customer_id == "SYN-CUST-001"
