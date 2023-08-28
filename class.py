from dataclasses import dataclass
from typing import Dict

@dataclass
class World:
    Plot:str
    History:str
    locations: Dict[str, str] 
    groups: Dict[str, str] 
    magic_system: str = None
    mcguffins: Dict[str, str] = None
    characters: Dict[str, str] = None