from dataclasses import dataclass

@dataclass(frozen=True)
class Coords:
    deg_lat: float
    deg_long: float

    def lat_to_string(self):
        if self.deg_lat > 0:
            side = "N"
        else:
            side = "S"
        return f"{side}{self.deg_lat}"

    def long_to_string(self):
        if self.deg_long > 0:
            side = "E"
        else:
            side = "W"
        return f"{side}{self.deg_long}"


    
@dataclass(frozen=True)
class Waypoint:
    name: str
    coords: Coords
    obj_type: str
    alt: float
    cap_d: int = None
    pente_d: float = None