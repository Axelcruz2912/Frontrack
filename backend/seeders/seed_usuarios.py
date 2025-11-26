import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.models.usuarios import create_usuario

def run():
    create_usuario("Super-Admin", "admin@bonafont.com", "admin", "123456")
    create_usuario("empleado ejemplo", "empleado@bonafont.com", "empleado", "123456")

if __name__ == "__main__":
    run()
