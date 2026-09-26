"""
OpenTAF Document Agent

Assesses synthetic customer document verification status.
"""

from opentaf.agents.base import Agent
from opentaf.agents.context import AgentExecutionContext
from opentaf.data.customer_repository import CustomerRepository


class DocumentAgent(Agent):
    """Agent responsible for document verification assessment."""

    def __init__(
        self,
        customer_repository: CustomerRepository,
    ) -> None:
        self._customer_repository = customer_repository

    @property
    def agent_id(self) -> str:
        return "OTAF-DOCUMENT-001"

    def execute(
        self,
        context: AgentExecutionContext,
    ) -> str:
        """Assess document verification status."""

        customer_id = context.data.get("customer_id")

        if customer_id is None:
            result = "customer_id_missing"

        else:
            customer = self._customer_repository.get(
                customer_id
            )

            if customer is None:
                result = "customer_not_found"

            elif customer.document_verified:
                result = "documents_verified"

            else:
                result = "document_verification_required"

        context.add_result(
            self.agent_id,
            result,
        )

        return result
