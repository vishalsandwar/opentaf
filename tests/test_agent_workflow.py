from opentaf.agents.base import Agent
from opentaf.agents.context import AgentExecutionContext
from opentaf.orchestration.agent_workflow import AgentWorkflow


class SyntheticAgent(Agent):
    def __init__(
        self,
        identifier: str,
        result: str,
    ):
        self._agent_id = identifier
        self._result = result

    @property
    def agent_id(self) -> str:
        return self._agent_id

    def execute(
        self,
        context: AgentExecutionContext,
    ) -> str:
        context.add_result(
            self.agent_id,
            self._result,
        )

        return self._result


def create_context():
    return AgentExecutionContext(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
    )


def test_workflow_executes_agents_in_sequence():
    first = SyntheticAgent(
        "OTAF-AGENT-001",
        "first_complete",
    )

    second = SyntheticAgent(
        "OTAF-AGENT-002",
        "second_complete",
    )

    workflow = AgentWorkflow(
        [
            first,
            second,
        ]
    )

    result = workflow.execute(
        create_context()
    )

    assert result.status == "completed"

    assert result.completed_agents == [
        "OTAF-AGENT-001",
        "OTAF-AGENT-002",
    ]


def test_workflow_collects_agent_results():
    first = SyntheticAgent(
        "OTAF-AGENT-001",
        "first_complete",
    )

    second = SyntheticAgent(
        "OTAF-AGENT-002",
        "second_complete",
    )

    workflow = AgentWorkflow(
        [
            first,
            second,
        ]
    )

    result = workflow.execute(
        create_context()
    )

    assert (
        result.results["OTAF-AGENT-001"]
        == "first_complete"
    )

    assert (
        result.results["OTAF-AGENT-002"]
        == "second_complete"
    )


def test_workflow_uses_shared_execution_context():
    class ContextAwareAgent(Agent):
        @property
        def agent_id(self):
            return "OTAF-CONTEXT-001"

        def execute(self, context):
            context.add_result(
                self.agent_id,
                "context_received",
            )

            return "context_received"

    workflow = AgentWorkflow(
        [
            ContextAwareAgent(),
        ]
    )

    context = create_context()

    result = workflow.execute(context)

    assert (
        result.results["OTAF-CONTEXT-001"]
        == "context_received"
    )

    assert (
        context.get_result(
            "OTAF-CONTEXT-001"
        )
        == "context_received"
    )
