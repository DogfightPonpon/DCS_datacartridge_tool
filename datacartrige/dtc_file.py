from dataclasses import dataclass
from enum import Enum
from typing import List
from waypoint import Waypoint

class Aircraft(Enum):
    M2000C = "M-2000C"

class Terrain(Enum):
    CAUCASUS = "Caucasus"

@dataclass()
class DTC_file:
    name: str
    filename: str
    terrain: Terrain
    aircraft: Aircraft
    wp_list: List[Waypoint]
    date: str = "01/01/2023"
    
    def write_to_file(self, file_name):
        file = open(file_name, "w")
        file.write("-- auto-generated datacartridge \n")
        file.write(f"terrain = \"{self.terrain.value}\"\n")
        file.write(f"aircraft = \"{self.aircraft.value}\"\n")
        file.write(f"date = \"{self.date}\"\n")
        file.write(f"name = \"{self.name}\"\n")

        file.write("waypoints = {} \n")
        wpt_number = 1
        for wpt in self.wp_list:
            file.write(f"waypoints[{wpt_number}] = {{ name=\"{wpt.name}\", lat=\"{wpt.coords.lat_to_string()}\", lon=\"{wpt.coords.lat_to_string()}\"}}\n")
            wpt_number += 1
        file.close()

    def add_wp(self):
        pass
    
    def add_wp_cap_d(self):
        pass
    
    def add_wp_pente_d(self):
        pass