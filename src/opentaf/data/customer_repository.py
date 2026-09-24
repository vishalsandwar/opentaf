"""
OpenTAF Customer Repository

Provides provider-independent access to synthetic customer data.
"""

from typing import Dict, List, Optional

from opentaf.models.customer import Customer


class CustomerRepository:
    """Repository for synthetic customer records."""

    def __init__(self) -> None:
        self._customers: Dict[str, Customer] = {}

    def save(self, customer: Customer) -> None:
        """Store a customer record."""

        self._customers[customer.customer_id] = customer

    def get(
        self,
        customer_id: str,
    ) -> Optional[Customer]:
        """Retrieve a customer by ID."""

        return self._customers.get(customer_id)

    def list_customers(self) -> List[Customer]:
        """Return all customers."""

        return list(self._customers.values())
