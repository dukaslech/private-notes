import dataset
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from criptografia import *
import random

"""ph = PasswordHasher()
# Hash de uma senha
hash = ph.hash("minha_senha_segura")
# Verificação
ph.verify(hash, "minha_senha_segura") # Retorna True"""



load_dotenv()

hashi = PasswordHasher()

DB_PATH = os.getenv('DB')


db = dataset.connect(DB_PATH)

users = db['users']
notes = db['notes']

def create_account(usernick, userpass):
    userid = random.randint(10000, 99999)
    if usernick == "" or userpass == "":
        return {"status": 400, "ok": False, "message": "Campos incompletos"}
    chk_nick = users.find_one(nick=usernick)
    if chk_nick != None:
        return {"status": 409, "ok": False, "message": "Nick já utilizado"}
    
    users.insert(dict(id=userid, nick=usernick, password=hashi.hash(userpass)))
    chk_nick = users.find_one(nick=usernick)
    if chk_nick == None:
        return {"status": 500, "ok": False, "message": "Erro inesperado do servidor!"}
    
    return {"status": 201, "ok": True, "message": "Conta criada com Sucesso"}