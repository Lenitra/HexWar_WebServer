from flask import Flask, jsonify
import os
import datetime
from flask import session
from datetime import timedelta
import time
import IA as ia
import threading


# this file path
here = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key =  os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10080)
# session.permanent = True

import routes.map
import routes.loginsys
import routes.web
import routes.leadder


def gameLoop():

    print("LOOP STARTED")

    UPDATE_IA_HOURS = [0, 6, 12, 18]

    UPDATE_PLAYER_CHECKS_COUNTDOWN = 5

    while True:
        # on récupère l'heure actuelle
        hour = datetime.datetime.now().hour
        minutes = datetime.datetime.now().minute

        # on vérifie si l'heure actuelle est dans la liste des heures de mise à jour de l'ia
        if hour in UPDATE_IA_HOURS and minutes == 0:
            try:
                iaCycle()
            except Exception as e:
                print(f"error: {e}")

        # on vérifie si le compte à rebours pour les vérifications des joueurs est terminé
        if minutes % UPDATE_PLAYER_CHECKS_COUNTDOWN == 0:
            usersChecks()

        # on attend la minute suivante
        now = datetime.datetime.now()
        next_minute = (now + datetime.timedelta(minutes=1)).replace(
            second=0, microsecond=0
        )
        time_to_sleep = (next_minute - now).total_seconds()

        time.sleep(time_to_sleep)


# fait jouer l'ia
def iaCycle():
    print("Mise à jour de l'IA")
    ia.aiCycle()


def usersChecks():
    print("Vérifications des utilisateurs")
    routes.map.check_hexes()


if __name__ == "__main__":
    if not os.getenv("WERKZEUG_RUN_MAIN"):  # Vérifie si c'est le processus principal
        gameLoopThread = threading.Thread(target=gameLoop)
        gameLoopThread.start()

    app.run(debug=True, host="0.0.0.0", port=8080)
