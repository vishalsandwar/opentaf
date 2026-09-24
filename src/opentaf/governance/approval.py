"""
OpenTAF Human Approval Service

Provides a provider-independent mechanism for managing
human approval decisions for governed agent actions.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ApprovalRequest:
    """Represents a request awaiting human approval."""

    approval_id: str
    request_id: str
    agent_id: str
    tool_id: str
    action: str
    requested_by: str
    reason: str
    status: str = "pending"
    decided_by: Optional[str] = None
    decision_reason: Optional[str] = None


class ApprovalService:
    """Manages human approval decisions."""

    def __init__(self) -> None:
        self._requests: Dict[str, ApprovalRequest] = {}

    def create_request(
        self,
        approval_id: str,
        request_id: str,
        agent_id: str,
        tool_id: str,
        action: str,
        requested_by: str,
        reason: str,
    ) -> ApprovalRequest:
        """Create a new approval request."""

        if approval_id in self._requests:
            raise ValueError(
                f"Approval request already exists: {approval_id}"
            )

        request = ApprovalRequest(
            approval_id=approval_id,
            request_id=request_id,
            agent_id=agent_id,
            tool_id=tool_id,
            action=action,
            requested_by=requested_by,
            reason=reason,
        )

        self._requests[approval_id] = request

        return request

    def get(
        self,
        approval_id: str,
    ) -> Optional[ApprovalRequest]:
        """Retrieve an approval request."""

        return self._requests.get(approval_id)

    def approve(
        self,
        approval_id: str,
        decided_by: str,
        decision_reason: str,
    ) -> ApprovalRequest:
        """Approve a pending request."""

        request = self.get(approval_id)

        if request is None:
            raise ValueError(
                f"Approval request not found: {approval_id}"
            )

        if request.status != "pending":
            raise ValueError(
                "Only pending approval requests can be approved."
            )

        request.status = "approved"
        request.decided_by = decided_by
        request.decision_reason = decision_reason

        return request

    def reject(
        self,
        approval_id: str,
        decided_by: str,
        decision_reason: str,
    ) -> ApprovalRequest:
        """Reject a pending request."""

        request = self.get(approval_id)

        if request is None:
            raise ValueError(
                f"Approval request not found: {approval_id}"
            )

        if request.status != "pending":
            raise ValueError(
                "Only pending approval requests can be rejected."
            )

        request.status = "rejected"
        request.decided_by = decided_by
        request.decision_reason = decision_reason

        return request
