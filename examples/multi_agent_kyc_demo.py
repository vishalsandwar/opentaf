"""
OpenTAF Multi-Agent KYC Workflow Demo

Demonstrates a deterministic multi-agent customer onboarding
workflow using synthetic enterprise data.
"""

from opentaf.agents.compliance import ComplianceAgent
from opentaf.agents.context import AgentExecutionContext
from opentaf.agents.document import DocumentAgent
from opentaf.agents.risk import RiskAgent
from opentaf.data.customer_repository import CustomerRepository
from opentaf.models.customer import Customer
from opentaf.orchestration.agent_workflow import AgentWorkflow


def main() -> None:
    # Synthetic enterprise data
    repository = CustomerRepository()

    repository.save(
        Customer(
            customer_id="SYN-CUST-001",
            full_name="Aarav Mehta",
            date_of_birth="1990-01-15",
            document_id="DOC-SYN-001",
            document_verified=True,
            kyc_status="pending",
        )
    )

    # Specialized agents
    document_agent = DocumentAgent(repository)
    risk_agent = RiskAgent(repository)
    compliance_agent = ComplianceAgent()

    # Deterministic workflow
    workflow = AgentWorkflow(
        [
            document_agent,
            risk_agent,
            compliance_agent,
        ]
    )

    context = AgentExecutionContext(
        request_id="REQ-KYC-MULTI-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
        data={
            "customer_id": "SYN-CUST-001",
        },
    )

    result = workflow.execute(context)

    print("OpenTAF Multi-Agent KYC Workflow")
    print("--------------------------------")
    print(f"Request: {result.request_id}")
    print(f"Status: {result.status}")
    print()
    print("Agent Results:")

    for agent_id, agent_result in result.results.items():
        print(f"- {agent_id}: {agent_result}")


if __name__ == "__main__":
    main()
