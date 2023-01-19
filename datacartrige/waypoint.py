from dataclasses import dataclass

@dataclass(frozen=True)
class Coords:
    deg_lat: float
    deg_long: float

    
@dataclass(frozen=True)
class Waypoint:
    name: str
    coords: Coords
    obj_type: str
    alt: float
    cap_d: int = None
    pente_d: float = None