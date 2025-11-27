import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from bson import ObjectId
from datetime import datetime, timedelta
from backend.db import get_db

db = get_db()
fallas = db["fallas"]

def run():
    lugar_id = "692189830fbcb73a9e516767"

    usuarios_reporta = [
        {"id": str(ObjectId()), "nombre": "Juan Pérez"},
        {"id": str(ObjectId()), "nombre": "María López"},
        {"id": str(ObjectId()), "nombre": "Carlos Gómez"},
    ]

    usuarios_revisa = [
        {"id": str(ObjectId()), "nombre": "Supervisor 1"},
        {"id": str(ObjectId()), "nombre": "Supervisor 2"},
        {"id": str(ObjectId()), "nombre": "Supervisor X"},
    ]

    autorizadores = [
        {"id": str(ObjectId()), "nombre": "Gerente General"},
        {"id": str(ObjectId()), "nombre": "Coordinador Operativo"},
    ]

    vehiculos = [
        {"id": "VH001", "modelo": "Nissan NP300", "placas": "ABC-123"},
        {"id": "VH002", "modelo": "Toyota Hilux", "placas": "XYZ-987"},
        {"id": "VH003", "modelo": "Ford Ranger", "placas": "JKL-456"},
    ]

    materiales = [
        {"id": "MAT001", "clave": "TV13AER", "descripcion": "Aerosol rojo", "cantidad": 1},
        {"id": "MAT002", "clave": "FILTACE001", "descripcion": "Filtro de aceite", "cantidad": 1},
        {"id": "MAT003", "clave": "BUJIAIRID", "descripcion": "Bujía iridium", "cantidad": 4},
    ]

    data = []

    for i in range(20):

        falla = {
            "_id": ObjectId(),
            "lugar_id": lugar_id,

            "usuario_reporta": usuarios_reporta[i % len(usuarios_reporta)],
            "usuario_revisa": usuarios_revisa[i % len(usuarios_revisa)],

            "vehiculo": vehiculos[i % len(vehiculos)],

            "fecha": datetime.utcnow() - timedelta(days=i),

            "nombre_conductor": f"Conductor {i+1}",
            "descripcion": f"Descripción de la falla número {i+1}",
            "observaciones": f"Observaciones adicionales {i+1}",

            "reviso_por": usuarios_revisa[i % len(usuarios_revisa)],

            "materiales_usados": [
                materiales[i % len(materiales)]
            ],

            "autorizado_por": autorizadores[i % len(autorizadores)],

            "correo_destino": f"correo{i+1}@bonafont.com",

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        data.append(falla)

    fallas.insert_many(data)
    print("Seeder de 20 fallas insertado correctamente.")

if __name__ == "__main__":
    run()
