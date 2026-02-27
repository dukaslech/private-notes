# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from db_functions import *
from flask import Response



def get_bearer_token() -> str | None:
    h = request.headers.get("Authorization", "")  # se não existir, vira ""
    if h.startswith("Bearer "):
        return h[7:].strip()
    return None


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

@app.post("/api/auth")
def auth():
    data = request.get_json(force=True)
    action = data.get("action", "")

    if action == "login":
        nick = data.get("nick", "")
        password = data.get("password", "")

        chk = login(nick, password)
        return jsonify(ok=chk["ok"], message=chk["message"], token=chk["token"]), chk["status"]

@app.get("/api/info/<token>")
def getinfo(token):
    if not token or token == "null":
        return Response("<h1>Token inválido</h1>", status=401, mimetype="text/html")
    return Response(str(get_accounts_info(token)), mimetype="text/html")


app.run(port=5098, debug=True)