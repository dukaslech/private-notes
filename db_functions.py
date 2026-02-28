import dataset
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from criptografia import *
import json
import random
import secrets
from argon2.exceptions import VerifyMismatchError
import random
import string

"""ph = PasswordHasher()
# Hash de uma senha
hash = ph.hash("minha_senha_segura")
# Verificação
ph.verify(hash, "minha_senha_segura") # Retorna True"""


campo_incompleto = {"status": 400, "ok": False, "message": "Campos incompletos", "token": "null"}
nick_utilizado = {"status": 409, "ok": False, "message": "Nick já utilizado", "token": "null"}
erro_inesperado = {"status": 500, "ok": False, "message": "Erro inesperado do servidor!", "token": "null"}
passuser_errado = {"status": 404, "ok": False, "message": "Info não existe!", "token": "null"}


load_dotenv()

def new_token():
    return secrets.token_urlsafe(32)

def note_id(length=8):
    """Generates a random alphanumeric ID of a specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

hashi = PasswordHasher()

DB_PATH = os.getenv('DB')
db = dataset.connect(DB_PATH)
users = db['users']
notes = db['notes']

def create_account(usernick, userpass):
    userid = random.randint(10000, 99999)
    if usernick == "" or userpass == "":
        return campo_incompleto
    chk_nick = users.find_one(nick=usernick)
    if chk_nick != None:
        return nick_utilizado
    
    users.insert(dict(id=userid, nick=usernick, password=hashi.hash(userpass)))
    chk_nick = users.find_one(nick=usernick)
    if chk_nick == None:
        return erro_inesperado
    
    return {"status": 201, "ok": True, "message": "Conta criada com Sucesso"}

def login(usernick, userpass):
    if usernick == "" or userpass == "":
        return campo_incompleto
    
    chk_nick = users.find_one(nick=usernick)
    if chk_nick == None:
        return passuser_errado

    row = users.find_one(nick=usernick)
    senha = row["password"]
    try:
        ok = hashi.verify(senha, userpass)
    except VerifyMismatchError:
        return passuser_errado

    token = new_token()
    users.update(dict(nick=usernick, token=token), ['nick'])

    return {"status": 200, "ok": True, "message": "Logado com sucesso!", "token": token}

def get_accounts_info(token):
    if not token or token == "null":
        return {"ok": False, "status": 401, "message": "Token inválido"}

    row = users.find_one(token=token)
    if row is None:
        return {"ok": False, "status": 401, "message": "Token inválido"}

    notas_rows = list(notes.find(user_id=row["id"]))
    notas = [{"id": n["id"], "title": n["title"]} for n in notas_rows]  # só id e título

    return {
        "ok": True,
        "status": 200,
        "user": {
            "id": row["id"],
            "nick": row["nick"],
            "token": row.get("token"),
        },
        "notes": notas
    }

def create_note(userid, title, body, passwordnote):
    if userid == "" or title == "" or body == "" or passwordnote == "":
        return campo_incompleto
    body = encrypt(body)
    passwordnote = hashi.hash(passwordnote)
    noteid = note_id()

    notes.insert(dict(id=noteid, user_id=userid, title=title, body=body, password=passwordnote))
    return {"status": 201, "ok": True, "message": "Nota criada com Sucesso"}


def read_note(noteid, password):
    if noteid == "" or password == "":
        return campo_incompleto
    chk = notes.find_one(id=noteid)
    if chk == None:
        return passuser_errado
    passhashed = chk["password"]
    try:
        ok = hashi.verify(passhashed, password)
    except VerifyMismatchError:
        return passuser_errado
    
    body = decrypt(chk["body"])
    title = chk["title"]

    return {
        "ok": True,
        "status": 200,
        "title": title,
        "body": body
    }

#print(get_accounts_info("Y2bqOJulYv_v6as0YguMhyq7tebAf9aVQJykuLkiWlM"))
#print(list(notes.all()))
#print(notes.find_one(id='sdadasd'))