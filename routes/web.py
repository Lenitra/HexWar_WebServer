from general import HERE, MAPSIZE  # pylint: disable=import-error
from __main__ import app
import json
from flask import render_template, request, session
from os import path
import datetime

# @app.route("/map", methods=["GET"])
# def map():
#     with open(HERE + "/data/users.json") as f:
#         users = json.load(f)
    
#     with open(HERE + "/data/map.json") as f:
#         map = json.load(f)

#     data = {}
#     for k, v in map.items():
#         data[k] = { "color" : "255|255|255", "name" : ""}
#         if v["owner"] != "":
#             data[k]["color"] = users[v["owner"]]["color"]
#             data[k]["owner"] = v["owner"]
#             data[k]["guild"] = users[v["owner"]]["guild"]

#     return render_template("map.html", data = data)

@app.route("/")
def index():
    return render_template("index.html")