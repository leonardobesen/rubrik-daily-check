"""Data source models for vCenter and Host entities."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from model.base import RubrikModel
from services.converter import iso_to_date

class ConnectionStatus(Enum):
    """Possible connection statuses for hosts."""
    CONNECTED = auto()
    DISCONNECTED = auto()
    UNKNOWN = auto()

    @classmethod
    def from_str(cls, status: str) -> 'ConnectionStatus':
        """Convert string status to enum value."""
        try:
            return cls[status.upper()]
        except KeyError:
            return cls.UNKNOWN

class OSType(Enum):
    """Supported operating system types."""
    LINUX = auto()
    WINDOWS = auto()
    NAS = auto()
    UNKNOWN = auto()

    @classmethod
    def from_str(cls, os_type: str) -> 'OSType':
        """Convert string OS type to enum value."""
        try:
            return cls[os_type.upper()]
        except KeyError:
            return cls.UNKNOWN

@dataclass
class VCenter(RubrikModel):
    """
    Represents a vCenter Server connection.
    
    Attributes:
        name: Name of the vCenter server
        status: Current connection status
        status_message: Detailed status information
        last_refresh_time: Time of last successful refresh
        cluster_name: Associated Rubrik cluster name (stored in lowercase)
    """
    name: str
    status: str
    status_message: str
    last_refresh_time: datetime | None
    cluster_name: str

    def __post_init__(self):
        """Post-initialization processing."""
        if self.last_refresh_time and isinstance(self.last_refresh_time, str):
            self.last_refresh_time = iso_to_date(self.last_refresh_time)
        else:
            self.last_refresh_time = None
        self.cluster_name = self.cluster_name.lower()

    def __str__(self) -> str:
        """String representation of the vCenter."""
        return f"""\nVCenter(
            name={self.name}, 
            status={self.status}, 
            status_message={self.status_message},
            last_refresh_time={self.last_refresh_time},
            cluster={self.cluster_name}
        )"""

@dataclass
class Host(RubrikModel):
    """
    Represents a physical or virtual host.
    
    Attributes:
        id: Unique identifier for the host
        name: Host name
        connection_status: Current connection status
        os: Operating system type
        cluster_name: Associated Rubrik cluster name (stored in lowercase)
    """
    id: str
    name: str
    connection_status: ConnectionStatus
    os: OSType
    cluster_name: str

    def __post_init__(self):
        """Post-initialization processing."""
        if isinstance(self.connection_status, str):
            self.connection_status = ConnectionStatus.from_str(self.connection_status)
        if isinstance(self.os, str):
            self.os = OSType.from_str(self.os)
        self.cluster_name = self.cluster_name.lower()

    @property
    def is_connected(self) -> bool:
        """Check if the host is currently connected."""
        return self.connection_status == ConnectionStatus.CONNECTED

    def __str__(self) -> str:
        """String representation of the host."""
        return f"""\nHost(
            id={self.id}, 
            name={self.name}, 
            connection_status={self.connection_status.name},
            os={self.os.name},
            cluster_name={self.cluster_name}
        )"""
