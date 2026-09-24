from opentaf.governance.approval import ApprovalService


def create_approval_service():
    return ApprovalService()


def create_request(service):
    return service.create_request(
        approval_id="APR-001",
        request_id="REQ-001",
        agent_id="OTAF-KYC-001",
        tool_id="TOOL-KYC-VALIDATE",
        action="validate_kyc",
        requested_by="synthetic-user-001",
        reason="High-risk KYC validation requires human approval.",
    )


def test_approval_request_can_be_created():
    service = create_approval_service()

    request = create_request(service)

    assert request.approval_id == "APR-001"
    assert request.status == "pending"


def test_pending_request_can_be_approved():
    service = create_approval_service()

    create_request(service)

    result = service.approve(
        approval_id="APR-001",
        decided_by="synthetic-reviewer-001",
        decision_reason="KYC information reviewed and approved.",
    )

    assert result.status == "approved"
    assert result.decided_by == "synthetic-reviewer-001"


def test_pending_request_can_be_rejected():
    service = create_approval_service()

    create_request(service)

    result = service.reject(
        approval_id="APR-001",
        decided_by="synthetic-reviewer-001",
        decision_reason="KYC information requires correction.",
    )

    assert result.status == "rejected"
    assert result.decided_by == "synthetic-reviewer-001"


def test_approved_request_cannot_be_approved_again():
    service = create_approval_service()

    create_request(service)

    service.approve(
        approval_id="APR-001",
        decided_by="synthetic-reviewer-001",
        decision_reason="Approved.",
    )

    try:
        service.approve(
            approval_id="APR-001",
            decided_by="synthetic-reviewer-002",
            decision_reason="Second approval.",
        )
        assert False
    except ValueError:
        assert True


def test_rejected_request_cannot_be_approved():
    service = create_approval_service()

    create_request(service)

    service.reject(
        approval_id="APR-001",
        decided_by="synthetic-reviewer-001",
        decision_reason="Rejected.",
    )

    try:
        service.approve(
            approval_id="APR-001",
            decided_by="synthetic-reviewer-002",
            decision_reason="Attempted approval.",
        )
        assert False
    except ValueError:
        assert True
