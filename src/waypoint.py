class Coords:
    def __init__(self, lat:float, long:float) -> None:
        self._ded_lat = lat
        self._ded_long = long 

    @property
    def lat_degree(self):
        return self._ded_lat

    @property
    def long_degree(self):
        return self._ded_long
    
    
class Waypoint:
    def __init__(self, name:str, coords:Coords, objective_type:str, alt:float) -> None:
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
        print(f"{self._name} is type {self._obj_type} in N{self._coords.lat_degree}, " 
              f"E{self._coords.long_degree} at {self._alt} ft")