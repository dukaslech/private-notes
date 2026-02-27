import dataset
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from criptografia import *
import random
import secrets
from argon2.exceptions import VerifyMismatchError

"""ph = PasswordHasher()
# Hash de uma senha
hash = ph.hash("minha_senha_segura")
# Verificação
ph.verify(hash, "minha_senha_segura") # Retorna True"""


campo_incompleto = {"status": 400, "ok": False, "message": "Campos incompletos", "token": "null"}
nick_utilizado = {"status": 409, "ok": False, "message": "Nick já utilizado", "token": "null"}
erro_inesperado = {"status": 500, "ok": False, "message": "Erro inesperado do servidor!", "token": "null"}
passuser_errado = {"status": 404, "ok": False, "message": "Usuario não existe!", "token": "null"}


load_dotenv()

def new_token():
    return secrets.token_urlsafe(32)

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
    if token == "null":
        return passuser_errado
    row = users.find_one(token=token)
    nick = row["nick"]
    notas = notes.find(user_id=row["id"])
    return nick, list(notas)

#print(get_accounts_info("Y2bqOJulYv_v6as0YguMhyq7tebAf9aVQJykuLkiWlM"))