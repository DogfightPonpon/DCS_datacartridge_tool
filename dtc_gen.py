import csv
from typing import List

class Objective:
    def __init__(self, name:str, coords:List[str], objective_type:str, alt:float) -> None:
        self._name = name
        self._coords = coords
        self._obj_type = objective_type
        self._alt = alt 
    
    @property
    def name(self):
        return self._name
        
    @property
    def coords(self):
        return self._coords

    @property
    def obj_type(self):
        return self._obj_type

    @property
    def alt(self):
        return self._alt # in feet

    def print(self):
        print(f"{self._name} is type {self._obj_type} in N{self._coords[0]}, E{self._coords[1]} at {self._alt} ft")


def read_objective_list(filename: str) -> List[Objective]:
    objectives = list()
    with open(filename, "r") as f:
        file = csv.reader(f)
        next(file) # skip header
        for line in file:
            coords = line[5].split(' ')
            obj = Objective(line[0], coords, line[1], float(line[8]))
            objectives.append(obj)
            
    return objectives

if __name__ == "__main__":
    objectives = read_objective_list("Caucasus_80s_Objectives.csv")
    for obj in objectives:
        obj.print()
