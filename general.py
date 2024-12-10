# Global variables and functions

import os
import json


HERE = os.path.dirname(os.path.abspath(__file__))

with open(HERE + "/data/map.json") as f:
    map = json.load(f)
    
MAPSIZE = 0
for hex in map:
    x = int(hex.split(":")[0])
    if x > MAPSIZE:
        MAPSIZE = x

