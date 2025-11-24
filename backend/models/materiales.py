from datetime import datetime
from bson import ObjectId
from backend.db import get_db

db = get_db()
materiales = db["materiales"]
lugares = db["lugares"]  

def create_material(data):
    if "lugar_id" in data and data["lugar_id"]:
        lugar = lugares.find_one({"_id": ObjectId(data["lugar_id"])})
        if not lugar:
            raise ValueError("El lugar especificado no existe")
    
    data["_id"] = ObjectId()
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    materiales.insert_one(data)
    return data

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

def get_material_by_id(material_id):
    pipeline = [
        {"$match": {"_id": ObjectId(material_id)}},
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

def update_material(material_id, data):
    # Validar lugar si se está actualizando
    if "lugar_id" in data and data["lugar_id"]:
        lugar = lugares.find_one({"_id": ObjectId(data["lugar_id"])})
        if not lugar:
            raise ValueError("El lugar especificado no existe")
    
    data["updated_at"] = datetime.utcnow()
    materiales.update_one(
        {"_id": ObjectId(material_id)},
        {"$set": data}
    )
    return get_material_by_id(material_id)

def delete_material(material_id):
    materiales.delete_one({"_id": ObjectId(material_id)})
    return True


# FUNCIÓN PARA OBTENER LUGARES (SELECT)
def get_lugares_para_select():
    return list(lugares.find(
        {},
        {"nombre": 1, "estado": 1, "_id": 1}
    ).sort("nombre", 1))