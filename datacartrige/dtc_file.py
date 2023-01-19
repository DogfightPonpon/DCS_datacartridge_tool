from dataclasses import dataclass
from enum import Enum
from typing import List
from waypoint import Waypoint

class Aircraft(Enum):
    M2000C = "M-2000C"

class Terrain(Enum):
    CAUCASUS = "Caucasus"

@dataclass(frozen=True)
class DTC_file:
    name: str
    filename: str
    terrain: Terrain
    aircraft: Aircraft
    wp_list: List(Waypoint) = list()
    date: str = "01/01/2023"
    
    def write_to_file(self):
        pass
    
    def add_wp(self):
        pass
    
    def add_wp_cap_d(self):
        pass
    
    def add_wp_pente_d(self):
        pass