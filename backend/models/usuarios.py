from datetime import datetime, timedelta
import hashlib
import secrets
from bson import ObjectId
from backend.db import get_db

db = get_db()
usuarios = db["usuarios"]


# =========================
# 🔐 Utilidades
# =========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =========================
# 👤 CRUD básico de usuarios
# =========================

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


# =========================
# 🔁 Recuperación de contraseña
# =========================

def create_reset_token(correo):
    """Genera un token y lo guarda con expiración de 1 hora."""
    usuario = usuarios.find_one({"correo": correo})
    if not usuario:
        return None

    token = secrets.token_hex(32)
    expiration = datetime.utcnow() + timedelta(hours=1)

    usuarios.update_one(
        {"_id": usuario["_id"]},
        {"$set": {
            "reset_token": token,
            "reset_expiration": expiration
        }}
    )

    return token


def reset_password(token, new_password):
    """Verifica el token y actualiza la contraseña."""
    usuario = usuarios.find_one({
        "reset_token": token,
        "reset_expiration": {"$gt": datetime.utcnow()}
    })

    if not usuario:
        return False

    usuarios.update_one(
        {"_id": usuario["_id"]},
        {
            "$set": {
                "password": hash_password(new_password)
            },
            "$unset": {
                "reset_token": "",
                "reset_expiration": ""
            }
        }
    )

    return True
