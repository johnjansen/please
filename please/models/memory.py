from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CommandMemory:
    """Stores information about a command execution"""
    timestamp: datetime
    natural_command: str
    bash_command: str
    successful: bool
    result: Optional[str] = None
