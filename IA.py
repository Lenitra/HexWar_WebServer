from general import *
import json
import random


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
            if 0 <= col_offset < MAPSIZE and 0 <= row_offset < MAPSIZE:
                toret.append({"x": col_offset, "z": row_offset})
    return toret


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


def aiCycle():

    with open(HERE + "/data/map.json", "r") as f:
        map = json.load(f)

    # si il n'y a aucune case appartenant à IA, on en place une

    # on vérifie si il y a une case appartenant à IA
    has_tile = 0
    for k, v in map.items():
        if v["owner"] == "Nyx":
            has_tile += 1 

    # si il n'y a pas de case appartenant à IA, on en place une aléatoirement sur la carte
    while has_tile <= 15:

        for k, v in map.items():
            if v["owner"] == "Nyx":
                has_tile += 1 

        x = random.randint(0, MAPSIZE)
        y = random.randint(0, MAPSIZE)
        empty_zone = True
        if map[f"{x}:{y}"]["owner"] == "":
            for tile in get_adjacent_hexes(x, y):
                if map[f"{tile['x']}:{tile['z']}"]["owner"] != "":
                    empty_zone = False
        
        if empty_zone:
            map[f"{x}:{y}"]["owner"] = "Nyx"
            map[f"{x}:{y}"]["units"] = 5
            has_tile += 1
            for tile in get_adjacent_hexes(x, y):
                map[f"{tile['x']}:{tile['z']}"]["owner"] = "Nyx"
                map[f"{tile['x']}:{tile['z']}"]["units"] = 3
                map[f"{tile['x']}:{tile['z']}"]["type"] = ""




    # on récupère les cases appartenant à IA
    ia_tiles = {}
    for k, v in map.items():
        if v["owner"] == "Nyx":
            ia_tiles[k] = v

    for k, v in ia_tiles.items():

        # si toutes les tiles adjacentes sont déjà occupées par IA, on augmente leur nombre d'unités de 1 (75% de chance)
        if all([map[f"{tile['x']}:{tile['z']}"]["owner"] == "Nyx" for tile in get_adjacent_hexes(int(k.split(":")[0]), int(k.split(":")[1]))]):
            if random.random() < 0.75:
                map[k]["units"] += 1

        # on renforce toutes les cases appartenant à IA avec une certaine probabilité
        if random.random() < 0.25:
            map[k]["units"] += 1

        # Si il y a des cases adjacentes vides on va en choisir une et avec une certaine probabilité on va envoyer des unités dessus
        if any([map[f"{tile['x']}:{tile['z']}"]["owner"] == "" for tile in get_adjacent_hexes(int(k.split(":")[0]), int(k.split(":")[1]))]):
            # get a random empty tile
            empty_tiles = [tile for tile in get_adjacent_hexes(int(k.split(":")[0]), int(k.split(":")[1])) if map[f"{tile['x']}:{tile['z']}"]["owner"] == ""]
            target_tile = random.choice(empty_tiles)
            # len(empty_tiles) * 5 = entre 5 et 30 % de chance d'envoyer des unités
            if random.random() < len(empty_tiles) * 0.05 and map[k]["units"] > 5:
                map[f"{target_tile['x']}:{target_tile['z']}"]["owner"] = "Nyx"
                map[f"{target_tile['x']}:{target_tile['z']}"]["units"] = 1
                map[f"{target_tile['x']}:{target_tile['z']}"]["type"] = ""


        

    # Enregistrer les nouvelles infos de la map
    with open(HERE + "/data/map.json", "w") as f:
        json.dump(map, f, indent=4)


if __name__ == "__main__":
    aiCycle()