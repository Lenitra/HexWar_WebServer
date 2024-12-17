from general import HERE, MAPSIZE  # pylint: disable=import-error
from __main__ import app
import json
from flask import jsonify, session, request
from os import path
import datetime


@app.route("/get_all_map")
def game_state():
    # Retourne l'entièreté de la map
    with open(HERE + "/data/map.json") as f:
        game_data = json.load(f)
    game_data = {"hexes": game_data}
    return jsonify(game_data)


@app.route("/get_price/<string:type>/<int:lvl>")
def get_price(type, lvl):
    return jsonify(get_prices(type, lvl))


# Permet de construire un nouveau batiment ou d'en améliorer
@app.route("/buildbat/<string:tile>/<string:type>")
def build_bat(tile, type):
    username = session.get("username")

    if "username" not in session:
        return "error : login"

    hex_x = tile.split(":")[0]
    hex_z = tile.split(":")[1]
    bat_type = type.lower()

    with open(HERE + "/data/map.json", "r") as f:
        hexes = json.load(f)

    with open(HERE + "/data/users.json", "r") as f:
        users = json.load(f)

    if bat_type == "":
        bat_type = hexes[f"{hex_x}:{hex_z}"]["type"].split(":")[0].lower()

    # Vérifier si l'hexagone appartient au joueur
    if hexes[f"{hex_x}:{hex_z}"]["owner"] != session.get("username"):
        return "NOPE"

    # Vérifier si l'hexagone est vide
    if hexes[f"{hex_x}:{hex_z}"]["type"] == "":

        if users[username]["money"] < get_prices(bat_type, 1):
            return "NOPE"

        users[username]["money"] -= get_prices(bat_type, 1)
        hexes[f"{hex_x}:{hex_z}"]["type"] = f"{bat_type}:1"
        hexes[f"{hex_x}:{hex_z}"]["owner"] = username

    # Si il y a déjà un batiment
    else:
        lvl = int(hexes[f"{hex_x}:{hex_z}"]["type"].split(":")[1])
        bat_type = hexes[f"{hex_x}:{hex_z}"]["type"].split(":")[0].lower()
        if lvl >= 5:
            return "NOPE"

        if users[username]["money"] < get_prices(bat_type, lvl + 1):
            return "NOPE"

        users[username]["money"] -= get_prices(bat_type, lvl + 1)
        hexes[f"{hex_x}:{hex_z}"]["type"] = f"{bat_type}:{lvl+1}"
        hexes[f"{hex_x}:{hex_z}"]["owner"] = username

    with open(HERE + "/data/map.json", "w") as f:
        json.dump(hexes, f, indent=4)
    with open(HERE + "/data/users.json", "w") as f:
        json.dump(users, f, indent=4)

    return "OK"


def get_prices(type, lvl):
    type = type.lower()
    if type == "barrack":
        if lvl == 1:
            return 150
        if lvl == 2:
            return 300
        if lvl == 3:
            return 500
        if lvl == 4:
            return 800
        if lvl == 5:
            return 1500
    if type == "miner":
        if lvl == 1:
            return 75
        if lvl == 2:
            return 300
        if lvl == 3:
            return 500
        if lvl == 4:
            return 800
        if lvl == 5:
            return 1500
    if type == "radar":
        if lvl == 1:
            return 100
        if lvl == 2:
            return 300
        if lvl == 3:
            return 500
        if lvl == 4:
            return 800
        if lvl == 5:
            return 1500
    if type == "hq":
        if lvl == 1:
            return 0
        if lvl == 2:
            return 500
        if lvl == 3:
            return 1500
        if lvl == 4:
            return 3000
        if lvl == 5:
            return 5000
    return -1


# bouger les unités d'un hexagone à un autre
# @param origin: hexagone d'origine sous forme de string "x:z"
# @param destination: hexagone de destination sous forme de string "x:z"
# @param units: nombre d'unités à déplacer
# @return: True si le déplacement a réussi, False sinon
@app.route("/move_units/<string:origin>/<string:destination>/<int:units>")
def move_units(origin, destination, units):

    if "username" not in session:
        return "error : login"

    with open(HERE + "/data/map.json", "r") as f:
        hexes = json.load(f)

    # si les hexagones n'existent pas
    if origin not in hexes or destination not in hexes:
        return "NOPE"

    # si le nombre d'unités est suffisant sur l'hexagone d'origine
    if hexes[origin]["units"] < units:
        return "NOPE"

    if hexes[origin]["owner"] != session.get("username"):
        return "NOPE"

    # si le chemin n'existe pas
    if find_path(origin, destination, hexes[origin]["owner"]) == []:
        return "NOPE"

    # si l'hexagone de destination est un HQ et n'appartient pas au joueur
    if (
        hexes[destination]["type"].split(":")[0] == "hq"
        and hexes[destination]["owner"] != hexes[origin]["owner"]
    ):
        return "NOPE"

    # un déplacement d'unités va se faire
    hexes[origin]["units"] -= units

    # ATTAQUE
    # si les owner sont différents
    if hexes[origin]["owner"] != hexes[destination]["owner"]:

        hexes[destination]["units"] -= units

        if hexes[destination]["units"] < 0:
            hexes[destination]["units"] = abs(hexes[destination]["units"])
            hexes[destination]["owner"] = hexes[origin]["owner"]

    # DEPLACEMENT
    # sinon on déplace les unités
    else:
        hexes[destination]["units"] += units

    with open(HERE + "/data/map.json", "w") as f:
        json.dump(hexes, f, indent=4)

    return jsonify(find_path(origin, destination, hexes[origin]["owner"]))


# Pemret de récupérer les hexagones d'un joueur et ses adjacents en fonction de ses batiments
# ROUTE APPELEE PAR LE CLIENT REGULIEREMENT
# Route pour récupérer les hexagones d'un joueur et ses adjacents en fonction de ses bâtiments
@app.route("/get_hex/<string:player>")
def get_hex(player):

    if session.get("username") != player:
        return "error : login"

    update_resources(player)
    # Charger les hexagones
    with open(HERE + "/data/map.json", "r") as f:
        hexes = json.load(f)

    with open(HERE + "/data/users.json", "r") as f:
        users = json.load(f)

    money = users[player]["money"]

    # Créer une liste pour les hexagones du joueur
    result = {}

    # Parcourir tous les hexagones et enregistrer ceux du joueur
    for k, v in hexes.items():
        if v["owner"] == player:
            result[k] = v

    # Parcourir les hexagones du joueur et ajouter les hexagones adjacents
    tmp = result.copy()
    for k, v in tmp.items():
        current_radius = 2
        x, z = map(int, k.split(":"))

        if v["type"].startswith("radar:"):
            current_radius = int(v["type"].split(":")[1]) + 2

        # Obtenir les hexagones adjacents en fonction du rayon
        for adj in get_adjacent_hexes(x, z, radius=current_radius):
            key = f"{adj['x']}:{adj['z']}"
            if key not in result and key in hexes:
                result[key] = hexes[key]

    return jsonify(money, format_json_hexes(result))


# Fonction permettant de trouver un chemin vers une tile en bfs
# @param origin: hexagone d'origine sous forme de string "x:z"
# @param destination: hexagone de destination sous forme de string "x:z"
# @param player: nom du joueur
# @return: liste des hexagones à traverser pour atteindre la destination
def find_path(origin, destination, player=""):
    with open(HERE + "/data/map.json", "r") as f:
        hexes = json.load(f)

    if origin not in hexes or destination not in hexes:
        return []

    # Créer une liste pour les hexagones visités
    visited = []
    # Créer une liste pour les hexagones à visiter
    queue = [[origin]]

    # Tant qu'il reste des hexagones à visiter
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Si on a atteint la destination
        if node == destination:
            return path

        # Si on n'a pas encore visité cet hexagone
        if node not in visited:
            # Ajouter cet hexagone à la liste des visités
            visited.append(node)
            if hexes[node]["owner"] != player:
                continue

            for k in get_adjacent_hexes(*map(int, node.split(":"))):
                if k not in visited:
                    new_path = list(path)
                    new_path.append(f"{k['x']}:{k['z']}")
                    queue.append(new_path)

    return []


# Permet de formater les hexagones en JSON pour les envoyer au client
def format_json_hexes(hexes):

    with open(HERE + "/data/users.json", "r") as f:
        users = json.load(f)

    toret = {"hexes": []}

    for k, v in hexes.items():
        color = ""
        if v["owner"] != "":
            color = users[v["owner"]]["color"]
        

        toret["hexes"].append(
            {
                "key": k,
                "owner": v["owner"],
                "type": v["type"],
                "units": v["units"],
                "color": color,
            }
        )

    return toret


# update les ressources de toutes les tiles d'un joueur ainsi que son argent
# @param player: nom du joueur
def update_resources(player):

    max_accumulated_hours = 6

    with open(HERE + "/data/users.json", "r") as f:
        users = json.load(f)

    with open(HERE + "/data/map.json", "r") as f:
        hexes = json.load(f)

    deltatime = datetime.datetime.now() - datetime.datetime.strptime(
        users[player]["recdatetime"], "%Y-%m-%d %H:%M:%S"
    )
    deltatimehours = deltatime.total_seconds() / 3600
    if deltatimehours > max_accumulated_hours:
        deltatimehours = max_accumulated_hours
    if deltatimehours > 1:
        for k, v in hexes.items():
            if v["owner"] == player:

                # si c'est une barrack, on ajoute des unités
                # une unité par heure
                if v["type"].split(":")[0] == "barrack":
                    v["units"] += int(deltatimehours) * int(v["type"].split(":")[1])
                    print("added", int(deltatimehours), "units to", k)

                # si c'est une mine, on ajoute des ressources au joueur
                if v["type"].split(":")[0] == "miner":
                    users[player]["money"] += int(deltatimehours) * int(
                        v["type"].split(":")[1]
                    )

        # on laisse les minutes restantes (en gros division euclidienne)
        deltatime = deltatimehours - int(deltatimehours)
        users[player]["recdatetime"] = (
            datetime.datetime.now() - datetime.timedelta(hours=deltatime)
        ).strftime("%Y-%m-%d %H:%M:%S")

        with open(HERE + "/data/users.json", "w") as f:
            json.dump(users, f, indent=4)
        with open(HERE + "/data/map.json", "w") as f:
            json.dump(hexes, f, indent=4)
        return True


# Fonction auxiliaire pour obtenir les hexagones adjacents avec un rayon variable
# Fonctions de conversion entre les coordonnées offset (grille) et cubiques
def evenq_offset_to_cube(col, row):
    x = col
    z = row - (col // 2)
    y = -x - z
    return (x, y, z)


def cube_to_evenq_offset(x, y, z):
    col = x
    row = z + (x // 2)
    return (col, row)


# Fonction pour obtenir tous les hexagones dans un rayon donné
def get_adjacent_hexes(x, z, radius=1):
    toret = []
    cx, cy, cz = evenq_offset_to_cube(x, z)
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            dz = -dx - dy
            if abs(dz) > radius:
                continue
            nx = cx + dx
            ny = cy + dy
            nz = cz + dz
            col_offset, row_offset = cube_to_evenq_offset(nx, ny, nz)
            if 0 <= col_offset <= MAPSIZE and 0 <= row_offset <= MAPSIZE:
                toret.append({"x": col_offset, "z": row_offset})
    return toret
