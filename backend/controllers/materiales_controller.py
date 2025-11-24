from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from backend.db import get_db

db = get_db()
materiales = db["materiales"]
lugares = db["lugares"]  # Agregar colección de lugares


# CREATE
def create_material_controller(
    clave_material,
    descripcion,
    generico,
    clasificacion,
    existencia,
    costo_promedio,
    lugar_id
):
    # Validación de clave duplicada
    if materiales.find_one({"clave_material": clave_material}):
        return {"error": "La clave del material ya está registrada."}

    # Validar que el lugar exista
    if lugar_id:
        try:
            lugar = lugares.find_one({"_id": ObjectId(lugar_id)})
            if not lugar:
                return {"error": "El lugar seleccionado no existe."}
        except InvalidId:
            return {"error": "ID de lugar inválido."}

    material = {
        "_id": ObjectId(),
        "clave_material": clave_material,
        "descripcion": descripcion,
        "generico": generico,
        "clasificacion": clasificacion,
        "existencia": float(existencia),
        "costo_promedio": float(costo_promedio),
        "lugar_id": lugar_id if lugar_id else None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    materiales.insert_one(material)
    return {"success": True, "material": material}


# READ
def get_all_materiales():
    pipeline = [
        {
            "$lookup": {
                "from": "lugares",
                "localField": "lugar_id",
                "foreignField": "_id",
                "as": "lugar_info"
            }
        },
        {
            "$unwind": {
                "path": "$lugar_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$addFields": {
                "lugar_nombre": "$lugar_info.nombre",
                "lugar_estado": "$lugar_info.estado"
            }
        },
        {
            "$project": {
                "lugar_info": 0
            }
        },
        {"$sort": {"descripcion": 1}}
    ]
    return list(materiales.aggregate(pipeline))


def get_materiales_paginados(
    filtro_clave="",
    filtro_descripcion="",
    filtro_generico="",
    pagina=1,
    por_pagina=10
):
    query = {}

    if filtro_clave:
        query["clave_material"] = {"$regex": filtro_clave, "$options": "i"}

    if filtro_descripcion:
        query["descripcion"] = {"$regex": filtro_descripcion, "$options": "i"}

    if filtro_generico:
        query["generico"] = {"$regex": filtro_generico, "$options": "i"}

    # Pipeline con paginación
    pipeline = [
        {"$match": query},
        {
            "$lookup": {
                "from": "lugares",
                "localField": "lugar_id",
                "foreignField": "_id",
                "as": "lugar_info"
            }
        },
        {
            "$unwind": {
                "path": "$lugar_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$addFields": {
                "lugar_nombre": "$lugar_info.nombre",
                "lugar_estado": "$lugar_info.estado"
            }
        },
        {
            "$project": {
                "lugar_info": 0
            }
        },
        {"$sort": {"descripcion": 1}},
        {"$skip": (pagina - 1) * por_pagina},
        {"$limit": por_pagina}
    ]

    total = materiales.count_documents(query)
    items = list(materiales.aggregate(pipeline))

    return {
        "materiales": items,
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_paginas": (total + por_pagina - 1) // por_pagina
    }


def get_material_by_id(id_material):
    try:
        pipeline = [
            {"$match": {"_id": ObjectId(id_material)}},
            {
                "$lookup": {
                    "from": "lugares",
                    "localField": "lugar_id",
                    "foreignField": "_id",
                    "as": "lugar_info"
                }
            },
            {
                "$unwind": {
                    "path": "$lugar_info",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$addFields": {
                    "lugar_nombre": "$lugar_info.nombre",
                    "lugar_estado": "$lugar_info.estado"
                }
            },
            {
                "$project": {
                    "lugar_info": 0
                }
            }
        ]
        
        result = list(materiales.aggregate(pipeline))
        return result[0] if result else None
    except InvalidId:
        return None


def buscar_materiales(termino):
    query = {
        "$or": [
            {"clave_material": {"$regex": termino, "$options": "i"}},
            {"descripcion": {"$regex": termino, "$options": "i"}},
            {"generico": {"$regex": termino, "$options": "i"}}
        ]
    }
    
    pipeline = [
        {"$match": query},
        {
            "$lookup": {
                "from": "lugares",
                "localField": "lugar_id",
                "foreignField": "_id",
                "as": "lugar_info"
            }
        },
        {
            "$unwind": {
                "path": "$lugar_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$addFields": {
                "lugar_nombre": "$lugar_info.nombre",
                "lugar_estado": "$lugar_info.estado"
            }
        },
        {
            "$project": {
                "lugar_info": 0
            }
        },
        {"$sort": {"descripcion": 1}}
    ]
    
    return list(materiales.aggregate(pipeline))


# UPDATE
def update_material(
    id_material,
    clave_material,
    descripcion,
    generico,
    clasificacion,
    existencia,
    costo_promedio,
    lugar_id
):
    # Validar que el lugar exista
    if lugar_id:
        try:
            lugar = lugares.find_one({"_id": ObjectId(lugar_id)})
            if not lugar:
                return {"error": "El lugar seleccionado no existe."}
        except InvalidId:
            return {"error": "ID de lugar inválido."}

    update_data = {
        "clave_material": clave_material,
        "descripcion": descripcion,
        "generico": generico,
        "clasificacion": clasificacion,
        "existencia": float(existencia),
        "costo_promedio": float(costo_promedio),
        "lugar_id": lugar_id if lugar_id else None,
        "updated_at": datetime.utcnow()
    }

    materiales.update_one(
        {"_id": ObjectId(id_material)},
        {"$set": update_data}
    )

    return {"success": True}


# DELETE
def delete_material(id_material):
    materiales.delete_one({"_id": ObjectId(id_material)})
    return {"success": True}


# FUNCIÓN PARA OBTENER LUGARES (SELECT)
def get_lugares_para_materiales():
    return list(lugares.find(
        {},
        {"nombre": 1, "estado": 1, "_id": 1}
    ).sort("nombre", 1))