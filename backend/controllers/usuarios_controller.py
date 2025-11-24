from datetime import datetime
import hashlib
from bson import ObjectId
from backend.db import get_db

db = get_db()
usuarios = db["usuarios"]



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



# CREATE
def create_usuario_controller(nombre, correo, rol, password):
    if usuarios.find_one({"correo": correo}):
        return {"error": "El correo ya está registrado."}

    usuario = {
        "_id": ObjectId(),
        "nombre": nombre,
        "correo": correo,
        "rol": rol,
        "password": hash_password(password),
        "created_at": datetime.utcnow()
    }

    usuarios.insert_one(usuario)
    return {"success": True, "usuario": usuario}


# READ
def get_all_usuarios():
    return list(usuarios.find().sort("nombre", 1))


def get_usuarios_paginados(filtro_nombre="", filtro_correo="", filtro_rol="", pagina=1, por_pagina=10):
    query = {}
    
    if filtro_nombre:
        query["nombre"] = {"$regex": filtro_nombre, "$options": "i"}
    
    if filtro_correo:
        query["correo"] = {"$regex": filtro_correo, "$options": "i"}
    
    if filtro_rol:
        query["rol"] = filtro_rol
    
    # Calcular paginación
    skip = (pagina - 1) * por_pagina
    
    # Obtener total de documentos para paginación
    total = usuarios.count_documents(query)
    
    # Obtener usuarios paginados
    usuarios_lista = list(
        usuarios.find(query)
        .sort("nombre", 1)
        .skip(skip)
        .limit(por_pagina)
    )
    
    return {
        "usuarios": usuarios_lista,
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_paginas": (total + por_pagina - 1) // por_pagina
    }


def get_usuario_by_id(id_usuario):
    return usuarios.find_one({"_id": ObjectId(id_usuario)})


def buscar_usuarios(termino_busqueda):
    """Búsqueda general en nombre y correo"""
    query = {
        "$or": [
            {"nombre": {"$regex": termino_busqueda, "$options": "i"}},
            {"correo": {"$regex": termino_busqueda, "$options": "i"}}
        ]
    }
    return list(usuarios.find(query).sort("nombre", 1))


# UPDATE

def update_usuario(id_usuario, nombre, correo, rol, password=None):
    update_data = {
        "nombre": nombre,
        "correo": correo,
        "rol": rol
    }
    
    # Si se proporciona una nueva contraseña, actualizarla
    if password:
        update_data["password"] = hash_password(password)
    
    usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$set": update_data}
    )
    return {"success": True}


#
# DELETE
def delete_usuario(id_usuario):
    usuarios.delete_one({"_id": ObjectId(id_usuario)})
    return {"success": True}