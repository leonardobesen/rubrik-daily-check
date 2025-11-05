"""Security-related models for SSO certificates and service accounts."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from model.base import RubrikModel
from services.converter import iso_to_date

@dataclass
class SSOCertificate(RubrikModel):
    """
    Represents an SSO Certificate.
    
    Attributes:
        name: Name of the SSO provider
        expiration_date: Certificate expiration date
    """
    name: str
    expiration_date: datetime

    def __post_init__(self):
        """Post-initialization processing."""
        if isinstance(self.expiration_date, str):
            self.expiration_date = iso_to_date(self.expiration_date)

    @property
    def days_until_expiration(self) -> int:
        """Calculate days remaining until certificate expiration."""
        if not self.expiration_date:
            return 0
        delta = self.expiration_date - datetime.now()
        return max(0, delta.days)

    @property
    def is_expired(self) -> bool:
        """Check if the certificate is expired."""
        return self.days_until_expiration == 0

    @property
    def is_expiring_soon(self) -> bool:
        """Check if the certificate is expiring within 30 days."""
        return 0 < self.days_until_expiration <= 30

    def __str__(self) -> str:
        """String representation of the SSO Certificate."""
        status = "EXPIRED" if self.is_expired else (
            "EXPIRING SOON" if self.is_expiring_soon else "VALID"
        )
        return f"""\nSSOCertificate(
            name={self.name}, 
            expiration_date={self.expiration_date},
            days_until_expiration={self.days_until_expiration},
            status={status}
        )"""

@dataclass
class ServicesAccount(RubrikModel):
    """
    Represents a service account.
    
    Attributes:
        name: Account username
        description: Account description
        last_login: Time of last login
    """
    name: str
    description: str
    last_login: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization processing."""
        if isinstance(self.last_login, str):
            self.last_login = iso_to_date(self.last_login) if self.last_login else None

    @property
    def days_since_login(self) -> Optional[int]:
        """Calculate days since last login."""
        if not self.last_login:
            return None
        delta = datetime.now() - self.last_login
        return delta.days

    @property
    def needs_review(self) -> bool:
        """Check if account needs review (no login in 90 days)."""
        if not self.days_since_login:
            return True
        return self.days_since_login > 90

    def __str__(self) -> str:
        """String representation of the Service Account."""
        login_info = (
            f"{self.days_since_login} days ago"
            if self.days_since_login is not None
            else "Never"
        )
        status = "NEEDS REVIEW" if self.needs_review else "ACTIVE"
        return f"""\nServiceAccount(
            name={self.name}, 
            description={self.description},
            last_login={self.last_login},
            last_login_days={login_info},
            status={status}
        )"""
