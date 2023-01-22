import csv
from typing import List
from waypoint import Waypoint, Coords

class BF_CSV_Parser:
    def __init__(self, filename: str) -> None:
        self._objectives = self._read_objective_list(filename) 

    @property
    def objective_list(self):
        return self._objectives

    @property
    def objective_names(self):
        return [f"{obj.name} ({obj.obj_type})" for obj in self.objective_list]
    
    @staticmethod
    def _read_objective_list(filename: str) -> List[Waypoint]:
        objectives = list()
        with open(filename, "r") as f:
            file = csv.reader(f)
            next(file) # skip header
            for line in file:
                raw_coords = line[5].split(' ')
                coords = Coords(float(raw_coords[0]), float(raw_coords[1]))
                wp = Waypoint(line[0], coords, line[1], float(line[8]))
                objectives.append(wp)
                
        return objectives