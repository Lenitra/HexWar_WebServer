from flask import Flask, jsonify
import json
import os
import datetime
from flask import session
from datetime import timedelta

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







if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
