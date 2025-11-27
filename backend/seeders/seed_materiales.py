import sys
from bson import ObjectId
from datetime import datetime
from pathlib import Path

# Configuración del path y conexión a la base de datos
# Esta línea ayuda a resolver la estructura de módulos si se ejecuta desde el script
sys.path.insert(0, str(Path(__file__).resolve().parents[2])) 

# Importaciones específicas después de ajustar el path
# Asumiendo que 'backend.db' contiene la lógica para 'get_db()'
try:
    from backend.db import get_db
except ImportError as e:
    print(f"Error de importación de get_db: {e}")
    sys.exit(1)

# Conexión a la base de datos y selección de la colección
db = get_db()
materiales = db["materiales"]

def seed_materiales():
    """Inserta datos de materiales de prueba en la colección 'materiales'."""
    
    # 1. Crear el índice único para 'clave_material' si no existe
    # Esto previene la inserción de materiales duplicados basados en su clave.
    try:
        materiales.create_index("clave_material", unique=True)
        print("Índice único en 'clave_material' creado/verificado.")
    except Exception as e:
        # Esto podría fallar si ya existen duplicados en la colección (no solo en el seed)
        print(f"Advertencia: No se pudo crear el índice único: {e}")
        
    data = [
        {
        "_id": ObjectId(),
            "clave_material": "TV13AER",
            "descripcion": "AEROSOL ROJO",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 2,
            "costo_promedio": 121.15,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "V13AERT",
            "descripcion": "AEROSOL VERDE",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 2,
            "costo_promedio": 121.15,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # 🔧 MATERIALES DE MOTOR
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "LUB10W40",
            "descripcion": "ACEITE 10W-40 SINTÉTICO",
            "generico": "ACEITE",
            "clasificacion": "MOTOR",
            "existencia": 25,
            "costo_promedio": 89.90,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LUB5W30",
            "descripcion": "ACEITE 5W-30 SINTÉTICO",
            "generico": "ACEITE",
            "clasificacion": "MOTOR",
            "existencia": 18,
            "costo_promedio": 95.50,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LUB20W50",
            "descripcion": "ACEITE 20W-50 MINERAL",
            "generico": "ACEITE",
            "clasificacion": "MOTOR",
            "existencia": 30,
            "costo_promedio": 65.75,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "FILTACE001",
            "descripcion": "FILTRO DE ACEITE UNIVERSAL",
            "generico": "FILTRO",
            "clasificacion": "MOTOR",
            "existencia": 15,
            "costo_promedio": 55.45,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "FILTAIRE001",
            "descripcion": "FILTRO DE AIRE UNIVERSAL",
            "generico": "FILTRO",
            "clasificacion": "MOTOR",
            "existencia": 22,
            "costo_promedio": 48.30,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "FILTGAS001",
            "descripcion": "FILTRO DE GASOLINA UNIVERSAL",
            "generico": "FILTRO",
            "clasificacion": "MOTOR",
            "existencia": 12,
            "costo_promedio": 72.15,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # 🛑 SISTEMA DE FRENOS
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "PASTFREDEL",
            "descripcion": "PASTILLAS DE FRENO DELANTERAS",
            "generico": "PASTILLAS",
            "clasificacion": "FRENOS",
            "existencia": 8,
            "costo_promedio": 320.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "PASTFRETRA",
            "descripcion": "PASTILLAS DE FRENO TRASERAS",
            "generico": "PASTILLAS",
            "clasificacion": "FRENOS",
            "existencia": 6,
            "costo_promedio": 280.50,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "DISCOSDEL",
            "descripcion": "DISCOS DE FRENO DELANTEROS",
            "generico": "DISCOS",
            "clasificacion": "FRENOS",
            "existencia": 4,
            "costo_promedio": 450.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LIQFRE001",
            "descripcion": "LÍQUIDO DE FRENOS DOT-4",
            "generico": "LÍQUIDO DE FRENOS",
            "clasificacion": "FRENOS",
            "existencia": 12,
            "costo_promedio": 43.25,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LIQFRE002",
            "descripcion": "LÍQUIDO DE FRENOS DOT-3",
            "generico": "LÍQUIDO DE FRENOS",
            "clasificacion": "FRENOS",
            "existencia": 10,
            "costo_promedio": 38.75,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # 🔋 SISTEMA ELÉCTRICO
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "BATERIA12V",
            "descripcion": "BATERÍA 12V 600A",
            "generico": "BATERÍA",
            "clasificacion": "ELÉCTRICO",
            "existencia": 4,
            "costo_promedio": 1150.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "BATERIA12V2",
            "descripcion": "BATERÍA 12V 700A",
            "generico": "BATERÍA",
            "clasificacion": "ELÉCTRICO",
            "existencia": 3,
            "costo_promedio": 1350.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "ALTERNADOR",
            "descripcion": "ALTERNADOR UNIVERSAL",
            "generico": "ALTERNADOR",
            "clasificacion": "ELÉCTRICO",
            "existencia": 2,
            "costo_promedio": 1200.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "MOTARRAQUE",
            "descripcion": "MOTOR DE ARRANQUE",
            "generico": "MOTOR ARRANQUE",
            "clasificacion": "ELÉCTRICO",
            "existencia": 2,
            "costo_promedio": 950.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "BUJIACOBRE",
            "descripcion": "BUJÍA DE COBRE STANDARD",
            "generico": "BUJÍA",
            "clasificacion": "ENCENDIDO",
            "existencia": 50,
            "costo_promedio": 85.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "BUJIAIRID",
            "descripcion": "BUJÍA IRIDIUM NGK",
            "generico": "BUJÍA",
            "clasificacion": "ENCENDIDO",
            "existencia": 30,
            "costo_promedio": 150.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "BUJIAPLAT",
            "descripcion": "BUJÍA PLATINO BOSCH",
            "generico": "BUJÍA",
            "clasificacion": "ENCENDIDO",
            "existencia": 25,
            "costo_promedio": 120.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # ❄️ SISTEMA DE ENFRIAMIENTO
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "ANTICONG01",
            "descripcion": "ANTICONGELANTE VERDE 1L",
            "generico": "ANTICONGELANTE",
            "clasificacion": "ENFRIAMIENTO",
            "existencia": 20,
            "costo_promedio": 67.80,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "ANTICONG02",
            "descripcion": "ANTICONGELANTE NARANJA 1L",
            "generico": "ANTICONGELANTE",
            "clasificacion": "ENFRIAMIENTO",
            "existencia": 15,
            "costo_promedio": 72.50,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "RADIADORUNI",
            "descripcion": "RADIADOR UNIVERSAL",
            "generico": "RADIADOR",
            "clasificacion": "ENFRIAMIENTO",
            "existencia": 3,
            "costo_promedio": 850.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "MANGUERAAG",
            "descripcion": "MANGUERA DE AGUA",
            "generico": "MANGUERA",
            "clasificacion": "ENFRIAMIENTO",
            "existencia": 8,
            "costo_promedio": 45.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "TERMOSTATO",
            "descripcion": "TERMOSTATO UNIVERSAL",
            "generico": "TERMOSTATO",
            "clasificacion": "ENFRIAMIENTO",
            "existencia": 10,
            "costo_promedio": 120.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # 🛞 SUSPENSIÓN Y DIRECCIÓN
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "AMORTDEL",
            "descripcion": "AMORTIGUADOR DELANTERO",
            "generico": "AMORTIGUADOR",
            "clasificacion": "SUSPENSION",
            "existencia": 6,
            "costo_promedio": 380.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "AMORTTRA",
            "descripcion": "AMORTIGUADOR TRASERO",
            "generico": "AMORTIGUADOR",
            "clasificacion": "SUSPENSION",
            "existencia": 6,
            "costo_promedio": 320.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "ROTULAEXT",
            "descripcion": "ROTULA EXTERIOR",
            "generico": "ROTULA",
            "clasificacion": "DIRECCION",
            "existencia": 12,
            "costo_promedio": 95.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "ROTULAINT",
            "descripcion": "ROTULA INTERIOR",
            "generico": "ROTULA",
            "clasificacion": "DIRECCION",
            "existencia": 12,
            "costo_promedio": 110.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "TERMINALDIR",
            "descripcion": "TERMINAL DE DIRECCIÓN",
            "generico": "TERMINAL",
            "clasificacion": "DIRECCION",
            "existencia": 15,
            "costo_promedio": 75.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # 🎨 CARROCERÍA Y PINTURA
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "AEROSOLAZUL",
            "descripcion": "AEROSOL AZUL METÁLICO",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 5,
            "costo_promedio": 121.15,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "AEROSOLNEG",
            "descripcion": "AEROSOL NEGRO MATE",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 4,
            "costo_promedio": 121.15,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "AEROSOLBLA",
            "descripcion": "AEROSOL BLANCO PERLA",
            "generico": "AEROSOL",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 3,
            "costo_promedio": 135.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "MASILLAEPO",
            "descripcion": "MASILLA EPOXICA 1KG",
            "generico": "MASILLA",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 8,
            "costo_promedio": 89.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LIJAGRA120",
            "descripcion": "LIJA GRANO 120",
            "generico": "LIJA",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 25,
            "costo_promedio": 12.50,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LIJAGRA400",
            "descripcion": "LIJA GRANO 400",
            "generico": "LIJA",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 20,
            "costo_promedio": 15.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LIJAGRA800",
            "descripcion": "LIJA GRANO 800",
            "generico": "LIJA",
            "clasificacion": "CARROCERIA Y PINTURA",
            "existencia": 18,
            "costo_promedio": 18.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },

        # ---------------------------------------------------------
        # 🔧 HERRAMIENTAS Y CONSUMIBLES
        # ---------------------------------------------------------
        {
            "_id": ObjectId(),
            "clave_material": "GRASALITIO",
            "descripcion": "GRASA DE LITIO 400G",
            "generico": "GRASA",
            "clasificacion": "LUBRICANTES",
            "existencia": 15,
            "costo_promedio": 45.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "SILICONA300",
            "descripcion": "SILICONA NEUTRA 300ML",
            "generico": "SILICONA",
            "clasificacion": "SELLADORES",
            "existencia": 10,
            "costo_promedio": 38.50,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "CINTAELEC",
            "descripcion": "CINTA AISLANTE NEGRA",
            "generico": "CINTA",
            "clasificacion": "ELECTRICO",
            "existencia": 30,
            "costo_promedio": 25.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "FUSIBLE20A",
            "descripcion": "FUSIBLE 20 AMPERES",
            "generico": "FUSIBLE",
            "clasificacion": "ELECTRICO",
            "existencia": 50,
            "costo_promedio": 8.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "FUSIBLE30A",
            "descripcion": "FUSIBLE 30 AMPERES",
            "generico": "FUSIBLE",
            "clasificacion": "ELECTRICO",
            "existencia": 40,
            "costo_promedio": 10.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "LIMPIACONT",
            "descripcion": "LIMPIADOR DE CONTACTOS 200ML",
            "generico": "LIMPIADOR",
            "clasificacion": "LIMPIEZA",
            "existencia": 12,
            "costo_promedio": 65.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "_id": ObjectId(),
            "clave_material": "DESENGRAS",
            "descripcion": "DESENGRASANTE 1L",
            "generico": "DESENGRASANTE",
            "clasificacion": "LIMPIEZA",
            "existencia": 8,
            "costo_promedio": 55.00,
            "lugar_id": "2",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]

    # Re-insertar los datos (aquí debes pegar el resto de la lista 'data' original)
    try:
        result = materiales.insert_many(data)
        print(f"✅ Seed de materiales insertado correctamente. Total: {len(result.inserted_ids)} registros.")
    except Exception as e:
        print(f"❌ Error al insertar datos. Es posible que ya existan documentos con la misma 'clave_material'. Error: {e}")

if __name__ == "__main__":
    seed_materiales()