from opentaf.agents.base import Agent
from opentaf.agents.context import AgentExecutionContext


class SyntheticAgent(Agent):
    @property
    def agent_id(self) -> str:
        return "OTAF-SYNTHETIC-001"

    def execute(
        self,
        context: AgentExecutionContext,
    ) -> str:
        result = (
            f"Processed request {context.request_id}"
        )

        context.add_result(
            self.agent_id,
            result,
        )

        return result


def create_context():
    return AgentExecutionContext(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
        data={
            "customer_id": "SYN-CUST-001",
        },
    )


def test_agent_has_unique_identifier():
    agent = SyntheticAgent()

    assert agent.agent_id == "OTAF-SYNTHETIC-001"


def test_agent_can_execute_against_context():
    agent = SyntheticAgent()
    context = create_context()

    result = agent.execute(context)

    assert result == (
        "Processed request REQ-001"
    )


def test_agent_result_is_added_to_context():
    agent = SyntheticAgent()
    context = create_context()

    agent.execute(context)

    assert (
        context.get_result(
            "OTAF-SYNTHETIC-001"
        )
        == "Processed request REQ-001"
    )
