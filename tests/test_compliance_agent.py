from opentaf.agents.compliance import ComplianceAgent
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


def test_compliance_is_clear_for_verified_low_risk_customer():
    agent = ComplianceAgent()

    context = create_context()

    context.add_result(
        "OTAF-DOCUMENT-001",
        "documents_verified",
    )

    context.add_result(
        "OTAF-RISK-001",
        "low_risk",
    )

    result = agent.execute(context)

    assert result == "compliance_clear"

    assert (
        context.get_result(
            "OTAF-COMPLIANCE-001"
        )
        == "compliance_clear"
    )


def test_compliance_requires_review_when_documents_are_not_verified():
    agent = ComplianceAgent()

    context = create_context()

    context.add_result(
        "OTAF-DOCUMENT-001",
        "document_verification_required",
    )

    context.add_result(
        "OTAF-RISK-001",
        "review_required",
    )

    result = agent.execute(context)

    assert result == "compliance_review_required"


def test_compliance_requires_review_when_risk_is_flagged():
    agent = ComplianceAgent()

    context = create_context()

    context.add_result(
        "OTAF-DOCUMENT-001",
        "documents_verified",
    )

    context.add_result(
        "OTAF-RISK-001",
        "risk_flagged",
    )

    result = agent.execute(context)

    assert result == "compliance_review_required"


def test_missing_document_result_is_detected():
    agent = ComplianceAgent()

    context = create_context()

    context.add_result(
        "OTAF-RISK-001",
        "low_risk",
    )

    result = agent.execute(context)

    assert result == "document_assessment_missing"


def test_missing_risk_result_is_detected():
    agent = ComplianceAgent()

    context = create_context()

    context.add_result(
        "OTAF-DOCUMENT-001",
        "documents_verified",
    )

    result = agent.execute(context)

    assert result == "risk_assessment_missing"
