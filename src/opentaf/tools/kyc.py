"""
OpenTAF KYC Validation Tool

Performs synthetic KYC validation against the
OpenTAF customer repository.
"""

from dataclasses import dataclass

from opentaf.data.customer_repository import CustomerRepository


@dataclass
class KYCValidationResult:
    """Result of a KYC validation operation."""

    customer_id: str
    status: str
    document_verified: bool
    risk_flag: str | None
    message: str


class KYCValidationTool:
    """Validates synthetic customer KYC information."""

    def __init__(
        self,
        customer_repository: CustomerRepository,
    ) -> None:
        self._customer_repository = customer_repository

    def validate(
        self,
        customer_id: str,
    ) -> KYCValidationResult:
        """Validate KYC information for a customer."""

        customer = self._customer_repository.get(
            customer_id
        )

        if customer is None:
            return KYCValidationResult(
                customer_id=customer_id,
                status="not_found",
                document_verified=False,
                risk_flag=None,
                message="Customer record not found.",
            )

        if not customer.document_verified:
            return KYCValidationResult(
                customer_id=customer.customer_id,
                status="review_required",
                document_verified=False,
                risk_flag=customer.risk_flag,
                message=(
                    "Customer document requires verification."
                ),
            )

        customer.kyc_status = "verified"

        return KYCValidationResult(
            customer_id=customer.customer_id,
            status="verified",
            document_verified=True,
            risk_flag=customer.risk_flag,
            message="Customer KYC successfully verified.",
        )
