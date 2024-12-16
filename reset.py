import json
import os 
import datetime

# this file path
here = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()


# WHAT TO REGENERATE
DEBUG = "units"

if DEBUG == "map" or DEBUG == "both":
    mapsize = 32
    map = {}



    for i in range (mapsize):
        for j in range(mapsize):
            map[f"{i}:{j}"] = {
                "owner": "",
                "type": "",
                "units": 0
            }

    # register map into data/map.json
    with open(here+"/data/map.json", "w") as f:
        json.dump(map, f, indent=4)


if DEBUG == "users" or DEBUG == "both":
    users = {
        "Lenitra": {
            "password": "password",
            "recdatetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        },
    }

    # register users into data/users.json
    with open(here+"/data/users.json", "w") as f:
        json.dump(users, f, indent=4)

if DEBUG == "units":
    # define units on every tile to 0
    with open(here+"/data/map.json", "r") as f:
        map = json.load(f)

    for k, v in map.items():
        v["units"] = 0

    # register units into data/map.json
    with open(here+"/data/map.json", "w") as f:
        json.dump(map, f, indent=4)