"""
OpenTAF Compliance Agent

Evaluates synthetic customer onboarding compliance using
results produced by upstream agents.
"""

from opentaf.agents.base import Agent
from opentaf.agents.context import AgentExecutionContext


class ComplianceAgent(Agent):
    """Agent responsible for compliance assessment."""

    @property
    def agent_id(self) -> str:
        return "OTAF-COMPLIANCE-001"

    def execute(
        self,
        context: AgentExecutionContext,
    ) -> str:
        """Evaluate compliance based on upstream results."""

        document_result = context.get_result(
            "OTAF-DOCUMENT-001"
        )

        risk_result = context.get_result(
            "OTAF-RISK-001"
        )

        if document_result is None:
            result = "document_assessment_missing"

        elif risk_result is None:
            result = "risk_assessment_missing"

        elif document_result != "documents_verified":
            result = "compliance_review_required"

        elif risk_result == "risk_flagged":
            result = "compliance_review_required"

        elif risk_result != "low_risk":
            result = "compliance_review_required"

        else:
            result = "compliance_clear"

        context.add_result(
            self.agent_id,
            result,
        )

        return result
