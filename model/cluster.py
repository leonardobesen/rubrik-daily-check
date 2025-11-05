"""Cluster model representing a Rubrik cluster."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from model.base import RubrikModel
from services.converter import iso_to_date, bytes_to_tb

@dataclass
class Cluster(RubrikModel):
    """
    Represents a Rubrik cluster with its properties and compliance information.
    
    Attributes:
        id: Unique identifier for the cluster
        name: Name of the cluster (stored in lowercase)
        system_status: Current system status
        pause_status: Pause status of the cluster
        status: Overall cluster status
        connected_state: Current connection state
        passed_connection_test: Whether the last connection test passed
        last_connection_time: Time of last successful connection
        total_capacity: Total storage capacity in TB
        used_capacity: Used storage capacity in TB
        snapshot_capacity: Storage used by snapshots in TB
        system_capacity: System storage usage in TB
        available_capacity: Available storage capacity in TB
        last_updated_time: Last time the cluster info was updated
        estimated_runaway: Estimated time until storage is full
        in_compliance_count: Number of objects in compliance
        out_of_compliance_count: Number of objects out of compliance
        compliance_pull_time: Last time compliance was checked
    """
    id: str
    name: str
    system_status: str
    pause_status: str
    status: str
    connected_state: str
    passed_connection_test: bool
    last_connection_time: datetime
    total_capacity: float
    used_capacity: float
    snapshot_capacity: float
    system_capacity: float
    available_capacity: float
    last_updated_time: datetime
    estimated_runaway: int
    in_compliance_count: int = field(default=0)
    out_of_compliance_count: int = field(default=0)
    compliance_pull_time: Optional[datetime] = None

    def __post_init__(self):
        """Post-initialization processing of data."""
        self.name = self.name.lower()
        self.last_connection_time = iso_to_date(self.last_connection_time)
        self.last_updated_time = iso_to_date(self.last_updated_time)
        
        # Convert storage values to TB
        self.total_capacity = bytes_to_tb(self.total_capacity)
        self.used_capacity = bytes_to_tb(self.used_capacity)
        self.snapshot_capacity = bytes_to_tb(self.snapshot_capacity)
        self.system_capacity = bytes_to_tb(self.system_capacity)
        self.available_capacity = bytes_to_tb(self.available_capacity)

    def set_in_compliance_count(self, count: int) -> None:
        """Set the number of objects in compliance."""
        self.in_compliance_count = count

    def set_out_of_compliance_count(self, count: int) -> None:
        """Set the number of objects out of compliance."""
        self.out_of_compliance_count = count

    def set_compliance_pull_time(self, iso_str: str) -> None:
        """Set the time when compliance information was last pulled."""
        self.compliance_pull_time = iso_to_date(iso_str)

    @property
    def total_objects(self) -> int:
        """Total number of objects tracked for compliance."""
        return self.in_compliance_count + self.out_of_compliance_count

    @property
    def compliance_percentage(self) -> float:
        """Percentage of objects in compliance."""
        if self.total_objects == 0:
            return 100.0
        return (self.in_compliance_count / self.total_objects) * 100

    def __str__(self) -> str:
        """String representation of the cluster."""
        return f"""\nCluster(
            id={self.id}, 
            name={self.name}, 
            status={self.status},
            passed_connection_test={self.passed_connection_test},
            last_connection={self.last_connection_time},
            total_capacity={self.total_capacity:.2f}TB,
            available_capacity={self.available_capacity:.2f}TB,
            in_compliance={self.in_compliance_count},
            out_of_compliance={self.out_of_compliance_count},
            compliance_percentage={self.compliance_percentage:.1f}%,
            pull_time={self.compliance_pull_time}
        )"""
