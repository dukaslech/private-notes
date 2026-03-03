from supabase import create_client, Client
import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
from criptografia import *
import json
import random
import secrets
from postgrest.exceptions import APIError
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


supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)


def create_account(usernick, userpass):
    userid = random.randint(10000, 99999)
    if usernick == "" or userpass == "":
        return campo_incompleto
    
    chk_nick = (
        supabase.table("users")
        .select("*")
        .eq("nick", usernick)
        .execute()
    )
    if chk_nick.data:
        return nick_utilizado


    response = (
        supabase.table("users")
        .insert({"id": userid, "nick":usernick, "password":hashi.hash(userpass)})
        .execute()
    )

    chk_nick = (
        supabase.table("users")
        .select("*")
        .eq("nick", usernick)
        .execute()
    )
    
    if chk_nick.data:
        return {"status": 201, "ok": True, "message": "Conta criada com Sucesso"}
    return erro_inesperado
    

def login(usernick, userpass):
    if usernick == "" or userpass == "":
        return campo_incompleto
    
    chk_nick = (
        supabase.table("users")
        .select("*")
        .eq("nick", usernick)
        .execute()
    )
    if chk_nick == None:
        return passuser_errado

    chk_pass = (
        supabase.table("users")
        .select("password")
        .eq("nick", usernick)
        .execute()
    )

    senha = chk_pass.data[0]["password"]
    try:
        ok = hashi.verify(senha, userpass)
    except VerifyMismatchError:
        return passuser_errado

    token = new_token()
    response = (
        supabase.table("users")
        .upsert({"nick":usernick, "token":token}, on_conflict="nick")
        .execute()
    )

    return {"status": 200, "ok": True, "message": "Logado com sucesso!", "token": token}

def get_accounts_info(token):
    if not token or token == "null":
        return {"ok": False, "status": 401, "message": "Token inválido"}

    usera = (
        supabase.table("users")
        .select("*")
        .eq("token", token)
        .execute()
    )
    if usera.data == []:
        return {"ok": False, "status": 401, "message": "Token inválido"}
    notas_rows = (
        supabase.table("notes")
        .select("*")
        .eq("user_id", usera.data[0]["id"])
        .execute()
    )

    notas = [{"id": n["id"], "title": n["title"]} for n in notas_rows.data]  # só id e título
    return {
        "ok": True,
        "status": 200,
        "user": {
            "id": usera.data[0]["id"],
            "nick": usera.data[0]["nick"],
            "token": usera.data[0]["token"],
        },
        "notes": notas
    }

def create_note(userid, title, body, passwordnote):
    if userid == "" or title == "" or body == "" or passwordnote == "":
        return campo_incompleto
    body = encrypt(body)
    passwordnote = hashi.hash(passwordnote)
    noteid = note_id()

    response = (
        supabase.table("notes")
        .insert({"id":noteid, "user_id":userid, "title":title, "body":body, "password":passwordnote})
        .execute()
    )
    return {"status": 201, "ok": True, "message": "Nota criada com Sucesso"}


def read_note(noteid, password):
    if noteid == "" or password == "":
        return campo_incompleto
    
    chk = (
        supabase.table("notes")
        .select("*")
        .eq("id", noteid)
        .execute()
    )

    if chk == []:
        return passuser_errado
    passhashed = chk.data[0]["password"]
    try:
        ok = hashi.verify(passhashed, password)
    except VerifyMismatchError:
        return passuser_errado
    
    body = decrypt(chk.data[0]["body"])
    title = chk.data[0]["title"]

    return {
        "ok": True,
        "status": 200,
        "title": title,
        "body": body
    }

