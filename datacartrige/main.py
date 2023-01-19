from parsers import BF_CSV_Parser
from dtc_file import *
from waypoint import *

if __name__ == "__main__":
    #bf80_caucasus = BF_CSV_Parser("data/Caucasus_80s_Objectives.csv")
    #objectives = bf80_caucasus.objective_list

    coord1 = Coords(deg_lat = 14.15478, deg_long = 46.1549674)
    coord2 = Coords(deg_lat = 64.41, deg_long = -75.0145)
    wpt1 = Waypoint(alt=493, name="waplt_1", coords = coord1, obj_type = "ARMY")
    wpt2 = Waypoint(alt=15453, name="waplt_2", coords = coord2, obj_type = "FARP")
    objs = {wpt1, wpt2}

    dtc = DTC_file(name = "autogen", filename = "autogen.dtc", terrain = Terrain.CAUCASUS, aircraft = Aircraft.M2000C, wp_list = objs)
    dtc.write_to_file(dtc.filename)
