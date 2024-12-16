from general import HERE
from __main__ import app
import json
from flask import jsonify, request, session
import os

@app.route("/login", methods=["POST"])
def login():
    with open(HERE + "/data/users.json") as f:
        users = json.load(f)

    data = request.get_json()
    if data["username"] in users and users[data["username"]]["password"] == data["password"]:
        session['username'] = data["username"]
        username = data["username"]
        color = users[username]["color"]
        money = users[username]["money"]
        return jsonify({"username": username, "color": color, "money": money})
    return "NOPE"





@app.route("/version", methods=["GET", "POST"])
def version():

    data = request.get_json()
    print(data)

    try:
        version = os.listdir(HERE + "/../builds")[0].split("_")[1]
    except:
        return "OK", 200
    
    if data["version"] != version:
        return "NOPE"
    
    return "OK", 200


@app.route("/get-version", methods=["GET"])
def get_version():
    try:
        version = os.listdir(HERE + "/static/builds")[0].split("_")[1]
    except:
        return jsonify({"version": "0.0.0"})

    return jsonify({"version": version})