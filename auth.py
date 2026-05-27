import requests
from database import buscar_usuario_por_email, criar_usuario

# SUA WEB API KEY DO FIREBASE
API_KEY = "AIzaSyAQxkQ8NchcMlqeAHhFF7T5slYxiP1I8O4"


# ========================
# CADASTRAR NO FIREBASE AUTH
# ========================

def registrar(nome, telefone, email, senha, tipo="aluno"):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"

    payload = {
        "email": email,
        "password": senha,
        "returnSecureToken": True
    }

    r = requests.post(url, json=payload)
    data = r.json()

    if "error" in data:
        return {
            "sucesso": False,
            "mensagem": data["error"]["message"]
        }

    uid = data["localId"]

    # salva dados extras no Firestore
    criar_usuario(
        uid=uid,
        nome=nome,
        telefone=telefone,
        email=email,
        tipo=tipo
    )

    return {
        "sucesso": True,
        "mensagem": "Conta criada com sucesso"
    }


# ========================
# LOGIN FIREBASE AUTH
# ========================

def login(email, senha):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

    payload = {
        "email": email,
        "password": senha,
        "returnSecureToken": True
    }

    r = requests.post(url, json=payload)
    data = r.json()

    if "error" in data:
        return {
            "sucesso": False,
            "mensagem": "Email ou senha inválidos"
        }

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return {
            "sucesso": False,
            "mensagem": "Usuário autenticado mas não encontrado no Firestore"
        }

    return {
        "sucesso": True,
        "usuario": usuario
    }