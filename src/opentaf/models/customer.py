"""
OpenTAF Synthetic Customer Model

Defines the synthetic customer information used by the
reference implementation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Represents a synthetic customer record."""

    customer_id: str
    full_name: str
    date_of_birth: str
    document_id: str
    document_verified: bool
    kyc_status: str
    risk_flag: Optional[str] = None
