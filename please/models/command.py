from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Command:
    """Represents a parsed natural language command"""
    action: str
    args: Dict[str, Any]
    raw_text: str
