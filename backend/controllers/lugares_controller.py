from datetime import datetime
from bson import ObjectId
from backend.db import get_db

db = get_db()
lugares = db["lugares"]


# CREATE
def create_lugar_controller(nombre, estado):

    # Validación de nombre duplicado
    if lugares.find_one({"nombre": nombre}):
        return {"error": "El lugar ya está registrado."}

    lugar = {
        "_id": ObjectId(),
        "nombre": nombre,
        "estado": estado,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    lugares.insert_one(lugar)
    return {"success": True, "lugar": lugar}


# READ
def get_all_lugares():
    return list(lugares.find().sort("nombre", 1))


def get_lugares_paginados(
    filtro_nombre="",
    filtro_estado="",
    pagina=1,
    por_pagina=10
):

    query = {}

    if filtro_nombre:
        query["nombre"] = {"$regex": filtro_nombre, "$options": "i"}

    if filtro_estado:
        query["estado"] = {"$regex": filtro_estado, "$options": "i"}

    # Paginación
    skip = (pagina - 1) * por_pagina
    total = lugares.count_documents(query)

    items = list(
        lugares.find(query)
        .sort("nombre", 1)
        .skip(skip)
        .limit(por_pagina)
    )

    return {
        "lugares": items,
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_paginas": (total + por_pagina - 1) // por_pagina
    }


def get_lugar_by_id(id_lugar):
    return lugares.find_one({"_id": ObjectId(id_lugar)})


def buscar_lugares(termino):
    query = {
        "$or": [
            {"nombre": {"$regex": termino, "$options": "i"}},
            {"estado": {"$regex": termino, "$options": "i"}},
        ]
    }
    return list(lugares.find(query).sort("nombre", 1))


# UPDATE

def update_lugar(id_lugar, nombre, estado):

    update_data = {
        "nombre": nombre,
        "estado": estado,
        "updated_at": datetime.utcnow()
    }

    lugares.update_one(
        {"_id": ObjectId(id_lugar)},
        {"$set": update_data}
    )

    return {"success": True}


# DELETE
def delete_lugar(id_lugar):
    lugares.delete_one({"_id": ObjectId(id_lugar)})
    return {"success": True}
