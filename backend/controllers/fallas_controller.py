from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from backend.db import get_db

db = get_db()
fallas = db["fallas"]
lugares = db["lugares"]
usuarios = db["usuarios"]
materiales = db["materiales"]


# CREATE
def create_falla_controller(
    lugar_id,
    usuario_reporta_id,
    usuario_revisa_id,
    fecha,
    nombre_conductor,
    descripcion,
    observaciones,
    reviso_por_id,
    materiales_usados,
    autorizado_por_id,
    correo_destino,
    vehiculo=None
):
    # Validaciones de referencias
    if not lugares.find_one({"_id": ObjectId(lugar_id)}):
        return {"error": "El lugar especificado no existe"}
    
    if not usuarios.find_one({"_id": ObjectId(usuario_reporta_id)}):
        return {"error": "El usuario que reporta no existe"}
    
    if usuario_revisa_id and not usuarios.find_one({"_id": ObjectId(usuario_revisa_id)}):
        return {"error": "El usuario que revisa no existe"}
    
    # Validar que reviso_por_id existe si se proporciona
    if reviso_por_id and not usuarios.find_one({"_id": ObjectId(reviso_por_id)}):
        return {"error": "El usuario que revisó no existe"}
    
    # Validar que autorizado_por_id existe si se proporciona
    if autorizado_por_id and not usuarios.find_one({"_id": ObjectId(autorizado_por_id)}):
        return {"error": "El usuario que autorizó no existe"}
    
    # Validar materiales si se proporcionan
    if materiales_usados:
        for material in materiales_usados:
            if "material_id" in material and not materiales.find_one({"_id": ObjectId(material["material_id"])}):
                return {"error": f"El material {material.get('material_id')} no existe"}

    # CONVERTIR fecha a datetime si es date
    if hasattr(fecha, 'strftime'):  # Si es date o datetime
        if not hasattr(fecha, 'hour'):  # Si es date (no tiene hora)
            fecha = datetime.combine(fecha, datetime.min.time())  # Convertir a datetime

    # Obtener información completa de los usuarios
    usuario_reporta = usuarios.find_one({"_id": ObjectId(usuario_reporta_id)})
    usuario_revisa = usuarios.find_one({"_id": ObjectId(usuario_revisa_id)}) if usuario_revisa_id else None
    usuario_reviso_por = usuarios.find_one({"_id": ObjectId(reviso_por_id)}) if reviso_por_id else None
    usuario_autorizado_por = usuarios.find_one({"_id": ObjectId(autorizado_por_id)}) if autorizado_por_id else None

    falla_data = {
        "_id": ObjectId(),
        "lugar_id": ObjectId(lugar_id),
        "usuario_reporta": {
            "_id": ObjectId(usuario_reporta_id),
            "nombre": usuario_reporta["nombre"],
            "correo": usuario_reporta["correo"],
            "rol": usuario_reporta["rol"]
        },
        "usuario_revisa": {
            "_id": ObjectId(usuario_revisa_id),
            "nombre": usuario_revisa["nombre"],
            "correo": usuario_revisa["correo"],
            "rol": usuario_revisa["rol"]
        } if usuario_revisa else None,
        "vehiculo": vehiculo or {},
        "fecha": fecha,  
        "nombre_conductor": nombre_conductor,
        "descripcion": descripcion,
        "observaciones": observaciones,
        "reviso_por": {
            "_id": ObjectId(reviso_por_id),
            "nombre": usuario_reviso_por["nombre"],
            "correo": usuario_reviso_por["correo"]
        } if usuario_reviso_por else None,
        "materiales_usados": materiales_usados or [],
        "autorizado_por": {
            "_id": ObjectId(autorizado_por_id),
            "nombre": usuario_autorizado_por["nombre"],
            "correo": usuario_autorizado_por["correo"]
        } if usuario_autorizado_por else None,
        "correo_destino": correo_destino,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    fallas.insert_one(falla_data)
    return {"success": True, "falla": falla_data}


# READ 
def get_all_fallas():
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
            "$lookup": {
                "from": "materiales",
                "localField": "materiales_usados.material_id",
                "foreignField": "_id",
                "as": "materiales_info"
            }
        },
        {
            "$addFields": {
                "lugar_nombre": "$lugar_info.nombre",
                "lugar_estado": "$lugar_info.estado",
                "materiales_usados": {
                    "$map": {
                        "input": "$materiales_usados",
                        "as": "material",
                        "in": {
                            "$mergeObjects": [
                                "$$material",
                                {
                                    "material_info": {
                                        "$arrayElemAt": [
                                            {
                                                "$filter": {
                                                    "input": "$materiales_info",
                                                    "as": "info",
                                                    "cond": {"$eq": ["$$info._id", "$$material.material_id"]}
                                                }
                                            },
                                            0
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "lugar_info": 0,
                "materiales_info": 0
            }
        },
        {"$sort": {"fecha": -1, "created_at": -1}}
    ]
    return list(fallas.aggregate(pipeline))


def get_fallas_paginadas(
    filtro_lugar="",
    filtro_descripcion="",
    filtro_conductor="",
    fecha_desde=None,
    fecha_hasta=None,
    pagina=1,
    por_pagina=10
):
    query = {}

    if filtro_lugar:
        # Buscar en lugares
        lugares_match = list(lugares.find(
            {"nombre": {"$regex": filtro_lugar, "$options": "i"}},
            {"_id": 1}
        ))
        lugar_ids = [lugar["_id"] for lugar in lugares_match]
        if lugar_ids:
            query["lugar_id"] = {"$in": lugar_ids}

    if filtro_descripcion:
        query["descripcion"] = {"$regex": filtro_descripcion, "$options": "i"}

    if filtro_conductor:
        query["nombre_conductor"] = {"$regex": filtro_conductor, "$options": "i"}

    if fecha_desde or fecha_hasta:
        query["fecha"] = {}
        if fecha_desde:
            if isinstance(fecha_desde, str):
                fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
            elif hasattr(fecha_desde, 'strftime') and not hasattr(fecha_desde, 'hour'):
                fecha_desde = datetime.combine(fecha_desde, datetime.min.time())
            query["fecha"]["$gte"] = fecha_desde
            
        if fecha_hasta:
            if isinstance(fecha_hasta, str):
                fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d")
            elif hasattr(fecha_hasta, 'strftime') and not hasattr(fecha_hasta, 'hour'):
                fecha_hasta = datetime.combine(fecha_hasta, datetime.max.time())
            query["fecha"]["$lte"] = fecha_hasta

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
            "$lookup": {
                "from": "materiales",
                "localField": "materiales_usados.material_id",
                "foreignField": "_id",
                "as": "materiales_info"
            }
        },
        {
            "$addFields": {
                "lugar_nombre": "$lugar_info.nombre",
                "lugar_estado": "$lugar_info.estado",
                "materiales_usados": {
                    "$map": {
                        "input": "$materiales_usados",
                        "as": "material",
                        "in": {
                            "$mergeObjects": [
                                "$$material",
                                {
                                    "material_info": {
                                        "$arrayElemAt": [
                                            {
                                                "$filter": {
                                                    "input": "$materiales_info",
                                                    "as": "info",
                                                    "cond": {"$eq": ["$$info._id", "$$material.material_id"]}
                                                }
                                            },
                                            0
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "lugar_info": 0,
                "materiales_info": 0
            }
        },
        {"$sort": {"fecha": -1, "created_at": -1}},
        {"$skip": (pagina - 1) * por_pagina},
        {"$limit": por_pagina}
    ]

    total = fallas.count_documents(query)
    items = list(fallas.aggregate(pipeline))

    return {
        "fallas": items,
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "total_paginas": (total + por_pagina - 1) // por_pagina
    }


def get_falla_by_id(id_falla):
    try:
        pipeline = [
            {"$match": {"_id": ObjectId(id_falla)}},
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
                "$lookup": {
                    "from": "materiales",
                    "localField": "materiales_usados.material_id",
                    "foreignField": "_id",
                    "as": "materiales_info"
                }
            },
            {
                "$addFields": {
                    "lugar_nombre": "$lugar_info.nombre",
                    "lugar_estado": "$lugar_info.estado",
                    "materiales_usados": {
                        "$map": {
                            "input": "$materiales_usados",
                            "as": "material",
                            "in": {
                                "$mergeObjects": [
                                    "$$material",
                                    {
                                        "material_info": {
                                            "$arrayElemAt": [
                                                {
                                                    "$filter": {
                                                        "input": "$materiales_info",
                                                        "as": "info",
                                                        "cond": {"$eq": ["$$info._id", "$$material.material_id"]}
                                                    }
                                                },
                                                0
                                            ]
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$project": {
                    "lugar_info": 0,
                    "materiales_info": 0
                }
            }
        ]
        
        result = list(fallas.aggregate(pipeline))
        return result[0] if result else None
    except InvalidId:
        return None


def buscar_fallas(termino):
    query = {
        "$or": [
            {"descripcion": {"$regex": termino, "$options": "i"}},
            {"observaciones": {"$regex": termino, "$options": "i"}},
            {"nombre_conductor": {"$regex": termino, "$options": "i"}},
            {"reviso_por.nombre": {"$regex": termino, "$options": "i"}},
            {"autorizado_por.nombre": {"$regex": termino, "$options": "i"}}
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
        {"$sort": {"fecha": -1}}
    ]
    
    return list(fallas.aggregate(pipeline))


# UPDATE
def update_falla(
    id_falla,
    lugar_id,
    usuario_reporta_id,
    usuario_revisa_id,
    fecha,
    nombre_conductor,
    descripcion,
    observaciones,
    reviso_por_id,
    materiales_usados,
    autorizado_por_id,
    correo_destino,
    vehiculo=None
):
    # Validaciones
    if not lugares.find_one({"_id": ObjectId(lugar_id)}):
        return {"error": "El lugar especificado no existe"}
    
    if not usuarios.find_one({"_id": ObjectId(usuario_reporta_id)}):
        return {"error": "El usuario que reporta no existe"}
    
    if usuario_revisa_id and not usuarios.find_one({"_id": ObjectId(usuario_revisa_id)}):
        return {"error": "El usuario que revisa no existe"}
    
    if reviso_por_id and not usuarios.find_one({"_id": ObjectId(reviso_por_id)}):
        return {"error": "El usuario que revisó no existe"}
    
    if autorizado_por_id and not usuarios.find_one({"_id": ObjectId(autorizado_por_id)}):
        return {"error": "El usuario que autorizó no existe"}

    if hasattr(fecha, 'strftime'):  
        if not hasattr(fecha, 'hour'):  
            fecha = datetime.combine(fecha, datetime.min.time())  

    usuario_reporta = usuarios.find_one({"_id": ObjectId(usuario_reporta_id)})
    usuario_revisa = usuarios.find_one({"_id": ObjectId(usuario_revisa_id)}) if usuario_revisa_id else None
    usuario_reviso_por = usuarios.find_one({"_id": ObjectId(reviso_por_id)}) if reviso_por_id else None
    usuario_autorizado_por = usuarios.find_one({"_id": ObjectId(autorizado_por_id)}) if autorizado_por_id else None

    update_data = {
        "lugar_id": ObjectId(lugar_id),
        "usuario_reporta": {
            "_id": ObjectId(usuario_reporta_id),
            "nombre": usuario_reporta["nombre"],
            "correo": usuario_reporta["correo"],
            "rol": usuario_reporta["rol"]
        },
        "usuario_revisa": {
            "_id": ObjectId(usuario_revisa_id),
            "nombre": usuario_revisa["nombre"],
            "correo": usuario_revisa["correo"],
            "rol": usuario_revisa["rol"]
        } if usuario_revisa else None,
        "vehiculo": vehiculo or {},
        "fecha": fecha,  # Ahora es datetime
        "nombre_conductor": nombre_conductor,
        "descripcion": descripcion,
        "observaciones": observaciones,
        "reviso_por": {
            "_id": ObjectId(reviso_por_id),
            "nombre": usuario_reviso_por["nombre"],
            "correo": usuario_reviso_por["correo"]
        } if usuario_reviso_por else None,
        "materiales_usados": materiales_usados or [],
        "autorizado_por": {
            "_id": ObjectId(autorizado_por_id),
            "nombre": usuario_autorizado_por["nombre"],
            "correo": usuario_autorizado_por["correo"]
        } if usuario_autorizado_por else None,
        "correo_destino": correo_destino,
        "updated_at": datetime.utcnow()
    }

    fallas.update_one(
        {"_id": ObjectId(id_falla)},
        {"$set": update_data}
    )

    return {"success": True}



# DELETE

def delete_falla(id_falla):
    fallas.delete_one({"_id": ObjectId(id_falla)})
    return {"success": True}


# FUNCIONES PARA DROPDOWNS
def get_lugares_para_fallas():
    return list(lugares.find({}, {"nombre": 1, "estado": 1, "_id": 1}).sort("nombre", 1))


def get_usuarios_para_fallas():
    return list(usuarios.find({}, {"nombre": 1, "correo": 1, "rol": 1, "_id": 1}).sort("nombre", 1))


def get_materiales_para_fallas():
    return list(materiales.find({}, {"clave_material": 1, "descripcion": 1, "existencia": 1, "_id": 1}).sort("descripcion", 1))