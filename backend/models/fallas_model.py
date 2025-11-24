from datetime import datetime
from bson import ObjectId
from backend.db import get_db

db = get_db()
fallas = db["fallas"]

def create_falla(data):
    data["_id"] = ObjectId()
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    fallas.insert_one(data)
    return data

def get_all_fallas():
    return list(fallas.find())

def get_falla_by_id(falla_id):
    return fallas.find_one({"_id": ObjectId(falla_id)})

def update_falla(falla_id, data):
    data["updated_at"] = datetime.utcnow()
    fallas.update_one(
        {"_id": ObjectId(falla_id)},
        {"$set": data}
    )
    return get_falla_by_id(falla_id)

def delete_falla(falla_id):
    fallas.delete_one({"_id": ObjectId(falla_id)})
    return True