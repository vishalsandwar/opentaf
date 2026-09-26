from opentaf.agents.context import AgentExecutionContext


def create_context():
    return AgentExecutionContext(
        request_id="REQ-001",
        user_id="synthetic-user-001",
        objective="Complete customer onboarding",
        data={
            "customer_id": "SYN-CUST-001",
        },
    )


def test_execution_context_can_be_created():
    context = create_context()

    assert context.request_id == "REQ-001"
    assert context.objective == "Complete customer onboarding"
    assert context.data["customer_id"] == "SYN-CUST-001"


def test_agent_result_can_be_added():
    context = create_context()

    context.add_result(
        "OTAF-DOCUMENT-001",
        "Documents verified",
    )

    assert (
        context.get_result("OTAF-DOCUMENT-001")
        == "Documents verified"
    )


def test_unknown_agent_result_returns_none():
    context = create_context()

    assert (
        context.get_result("OTAF-RISK-001")
        is None
    )
