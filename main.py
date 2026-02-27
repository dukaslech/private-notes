# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from db_functions import *


app = Flask(__name__)
#CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5173"}})

@app.post("/api/user")
def userapi():
    data = request.get_json(force=True)
    action = data.get("action", "")

    if action == "register":
        nick = data.get("nick", "")
        password = data.get("password", "")

        chk = create_account(nick, password)
        return jsonify(ok=chk["ok"], message=chk["message"]), chk["status"]


app.run(port=5098, debug=True)