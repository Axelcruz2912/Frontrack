import streamlit as st
from frontend.crud_usuarios import crud_usuarios
from frontend.fallas_view import crud_fallas
from frontend.crud_lugares import crud_lugares
from frontend.crud_materiales import crud_materiales

def crud_menu():

    #  Validación por login
    
    if "user" not in st.session_state:
        st.session_state["page"] = "login"
        st.rerun()

    rol = st.session_state["user"]["rol"]

    st.title("Gestión del Sistema")

    # OPCIONES POR ROL
    
    if rol == "admin":
        opciones = ["Usuarios", "Lugares", "Materiales", "Fallas"]
    else:  # Empleado
        opciones = ["Fallas"]  # ÚNICO CRUD PERMITIDO

    opcion = st.selectbox("Selecciona un módulo:", opciones)

    # CRUDs
    if opcion == "Usuarios" and rol == "admin":
        crud_usuarios()

    elif opcion == "Lugares" and rol == "admin":
        crud_lugares()

    elif opcion == "Materiales" and rol == "admin":
        crud_materiales()

    elif opcion == "Fallas":
        crud_fallas()

