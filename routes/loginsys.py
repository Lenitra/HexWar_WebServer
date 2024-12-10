from general import HERE
from __main__ import app
import json
from flask import jsonify, request, session
import datetime

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
