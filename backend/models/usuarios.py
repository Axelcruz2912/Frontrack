from datetime import datetime
import hashlib
from bson import ObjectId
from backend.db import get_db

db = get_db()
usuarios = db["usuarios"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_usuario(nombre, correo, rol, password):
    usuario = {
        "_id": ObjectId(),
        "nombre": nombre,
        "correo": correo,
        "rol": rol,
        "password": hash_password(password),
        "created_at": datetime.utcnow()
    }

    usuarios.insert_one(usuario)
    return usuario

def authenticate(correo, password):
    return usuarios.find_one({
        "correo": correo,
        "password": hash_password(password)
    })

def correo_existe(correo):
    return usuarios.find_one({"correo": correo}) is not None
