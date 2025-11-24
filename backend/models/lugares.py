from datetime import datetime
from bson import ObjectId
from backend.db import get_db

db = get_db()
lugares = db["lugares"]

def create_lugar(data):
    data["_id"] = ObjectId()
    data["created_at"] = datetime.utcnow()
    data["updated_at"] = datetime.utcnow()
    lugares.insert_one(data)
    return data

def get_all_lugares():
    return list(lugares.find())

def get_lugar_by_id(lugar_id):
    return lugares.find_one({"_id": ObjectId(lugar_id)})

def update_lugar(lugar_id, data):
    data["updated_at"] = datetime.utcnow()
    lugares.update_one(
        {"_id": ObjectId(lugar_id)},
        {"$set": data}
    )
    return get_lugar_by_id(lugar_id)

def delete_lugar(lugar_id):
    lugares.delete_one({"_id": ObjectId(lugar_id)})
    return True
