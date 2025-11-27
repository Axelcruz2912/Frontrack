import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.models.usuarios import create_usuario

def run():
    create_usuario("Super-Admin", "admin@bonafont.com", "admin", "123456")

    empleados = [
        ("Juan Pérez", "juan.perez@bonafont.com"),
        ("María López", "maria.lopez@bonafont.com"),
        ("Carlos Hernández", "carlos.hernandez@bonafont.com"),
        ("Ana Torres", "ana.torres@bonafont.com"),
        ("Luis Gómez", "luis.gomez@bonafont.com"),
        ("Laura Sánchez", "laura.sanchez@bonafont.com"),
        ("Miguel Rivera", "miguel.rivera@bonafont.com"),
        ("Patricia Ramos", "patricia.ramos@bonafont.com"),
        ("Daniel Romero", "daniel.romero@bonafont.com"),
        ("Karla Jiménez", "karla.jimenez@bonafont.com"),
        ("Hugo Castillo", "hugo.castillo@bonafont.com"),
        ("Elena Márquez", "elena.marquez@bonafont.com"),
        ("Fernando Ortiz", "fernando.ortiz@bonafont.com"),
        ("Gabriela Molina", "gabriela.molina@bonafont.com"),
        ("Ricardo Vargas", "ricardo.vargas@bonafont.com"),
        ("César Navarro", "cesar.navarro@bonafont.com"),
        ("Beatriz Flores", "beatriz.flores@bonafont.com"),
        ("Oscar Delgado", "oscar.delgado@bonafont.com"),
        ("Silvia Cabrera", "silvia.cabrera@bonafont.com"),
        ("Iván Domínguez", "ivan.dominguez@bonafont.com"),
    ]

    for nombre, correo in empleados:
        create_usuario(nombre, correo, "empleado", "123456")

    print("Seeder de 20 empleados ejecutado correctamente.")

if __name__ == "__main__":
    run()
