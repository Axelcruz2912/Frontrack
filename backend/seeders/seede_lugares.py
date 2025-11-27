from datetime import datetime
import sys
from pathlib import Path

# Ajuste de path para asegurar que la importación funcione
sys.path.insert(0, str(Path(__file__).resolve().parents[2])) 

# Importamos la función que realmente inserta en la base de datos
try:
    from backend.models.lugares import create_lugar
except ImportError as e:
    print(f"Error de importación: Asegúrate que backend.models.lugares existe y tiene la función create_lugar. Error: {e}")
    sys.exit(1)


def seed_lugares():
    """Siembra datos iniciales de CEDIS en México."""
    
    lugares_data = [
        # ZONA CENTRAL
        {
            "nombre": "CEDIS Centro - Ciudad de México",
            "estado": "Ciudad de México",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "nombre": "CEDIS Bajío - Guanajuato",
            "estado": "Guanajuato",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # ZONA OCCIDENTE
        {
            "nombre": "CEDIS Occidente - Guadalajara",
            "estado": "Jalisco",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # ZONA NORTE / NORESTE
        {
            "nombre": "CEDIS Norte - Monterrey",
            "estado": "Nuevo León",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "nombre": "CEDIS Noreste - Chihuahua",
            "estado": "Chihuahua",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # ZONA NOROESTE
        {
            "nombre": "CEDIS Noroeste - Tijuana",
            "estado": "Baja California",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        
        # ZONA SUR / SURESTE
        {
            "nombre": "CEDIS Sur - Oaxaca",
            "estado": "Oaxaca",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "nombre": "CEDIS Sureste - Mérida",
            "estado": "Yucatán",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "nombre": "CEDIS Caribe - Cancún",
            "estado": "Quintana Roo",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
    ]
    
    count = 0
    print("Iniciando siembra de lugares...")
    
    for lugar_data in lugares_data:
        try:
            # Se asume que create_lugar maneja la inserción en la DB (PyMongo o un ORM).
            create_lugar(lugar_data) 
            count += 1
        except Exception as e:
            # Captura errores de la DB, como duplicados.
            print(f"❌ Error al crear el lugar '{lugar_data['nombre']}': {e}")
    
    print(f"\n✅ **{count}** de **{len(lugares_data)}** CEDIS sembrados correctamente.")

if __name__ == "__main__":
    seed_lugares()