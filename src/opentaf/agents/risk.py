"""
OpenTAF Risk Agent

Assesses synthetic customer risk using results produced
by upstream agents and customer risk indicators.
"""

from opentaf.agents.base import Agent
from opentaf.agents.context import AgentExecutionContext
from opentaf.data.customer_repository import CustomerRepository


class RiskAgent(Agent):
    """Agent responsible for customer risk assessment."""

    def __init__(
        self,
        customer_repository: CustomerRepository,
    ) -> None:
        self._customer_repository = customer_repository

    @property
    def agent_id(self) -> str:
        return "OTAF-RISK-001"

    def execute(
        self,
        context: AgentExecutionContext,
    ) -> str:
        """Assess customer risk."""

        document_result = context.get_result(
            "OTAF-DOCUMENT-001"
        )

        customer_id = context.data.get(
            "customer_id"
        )

        if customer_id is None:
            result = "customer_id_missing"

        elif document_result is None:
            result = "document_assessment_missing"

        elif document_result != "documents_verified":
            result = "review_required"

        else:
            customer = self._customer_repository.get(
                customer_id
            )

            if customer is None:
                result = "customer_not_found"

            elif customer.risk_flag:
                result = "risk_flagged"

            else:
                result = "low_risk"

        context.add_result(
            self.agent_id,
            result,
        )

        return result
