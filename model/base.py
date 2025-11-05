"""Base model class for Rubrik entities."""

from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class RubrikModel:
    """Base class for all Rubrik models."""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RubrikModel':
        """
        Create an instance from a dictionary.
        
        Args:
            data: Dictionary containing model data
            
        Returns:
            An instance of the model
        """
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {k: str(v) if v is not None else None 
                for k, v in self.__dict__.items()}