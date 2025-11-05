"""Live Mount model representing mounted backups."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from model.base import RubrikModel
from services.converter import iso_to_date

class MountType(Enum):
    """Types of Live Mounts."""
    VM = auto()
    MSSQL = auto()
    ORACLE = auto()
    MANAGED_VOLUME = auto()
    UNKNOWN = auto()

    @classmethod
    def from_str(cls, mount_type: str) -> 'MountType':
        """Convert string mount type to enum value."""
        try:
            return cls[mount_type.upper()]
        except KeyError:
            return cls.UNKNOWN

@dataclass
class LiveMount(RubrikModel):
    """
    Represents a Live Mount of a backup.
    
    Attributes:
        id: Unique identifier for the mount
        name: Name of the mounted object
        date: Mount creation date
        type: Type of the mount (VM, MSSQL, etc.)
        cluster_name: Associated Rubrik cluster name (stored in lowercase)
    """
    id: str
    name: str
    date: datetime
    type: MountType
    cluster_name: str

    def __post_init__(self):
        """Post-initialization processing."""
        if isinstance(self.date, str):
            self.date = iso_to_date(self.date)
        if isinstance(self.type, str):
            self.type = MountType.from_str(self.type)
        self.cluster_name = self.cluster_name.lower()

    @property
    def mount_age_days(self) -> float:
        """Calculate the age of the mount in days."""
        if not self.date:
            return 0.0
        delta = datetime.now() - self.date
        return delta.total_seconds() / 86400  # Convert seconds to days

    def __str__(self) -> str:
        """String representation of the Live Mount."""
        return f"""\nLiveMount(
            id={self.id}, 
            name={self.name}, 
            mount_date={self.date},
            mount_age={self.mount_age_days:.1f} days,
            type={self.type.name},
            cluster={self.cluster_name}
        )"""
