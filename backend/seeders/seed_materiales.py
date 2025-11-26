import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.models.materiales import create_material

SAMPLE_MATERIALES = [
    {
        "nombre": "Filtro de agua 10\"",
        "codigo": "MAT-001",
        "unidad": "unidad",
        "existencia": 50,
        "descripcion": "Filtro de repuesto para plantas de tratamiento"
    },
    {
        "nombre": "Tubo PVC 3/4\"",
        "codigo": "MAT-002",
        "unidad": "metro",
        "existencia": 200,
        "descripcion": "Tubo PVC para conducción de agua"
    },
    {
        "nombre": "Válvula de bola 1\"",
        "codigo": "MAT-003",
        "unidad": "unidad",
        "existencia": 75,
        "descripcion": "Válvula de control de paso"
    }
]

def run():
    for m in SAMPLE_MATERIALES:
        try:
            # pasar copia para evitar mutar la constante en create_material
            created = create_material(m.copy())
            print(f"Material creado: {created.get('nombre')} ({created.get('_id')})")
        except Exception as e:
            print(f"Error creando material '{m.get('nombre')}': {e}")

if __name__ == "__main__":
    run()