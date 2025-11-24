import streamlit as st
import re
from backend.models.usuarios import create_usuario, get_usuario_by_correo

def registro():
    st.title("Registro de usuario")

    with st.form("form_registro"):
        nombre = st.text_input("Nombre completo")
        correo = st.text_input("Correo")
        password = st.text_input("Contraseña", type="password")
        confirmar = st.text_input("Confirmar contraseña", type="password")
        rol = st.selectbox("Rol", ["admin", "empleado"])

        enviar = st.form_submit_button("Crear cuenta")

    if enviar:

        # VALIDACIONES
        if not nombre or not correo or not password:
            st.error("Todos los campos son obligatorios")
            return
        
        # Validar correo
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            st.error("Correo inválido")
            return

        # Validar que no exista
        if get_usuario_by_correo(correo) is not None:
            st.error("Ese correo ya está registrado")
            return

        if password != confirmar:
            st.error("Las contraseñas no coinciden")
            return

        # GUARDAR EN DB
        user_id = create_usuario({
            "nombre": nombre,
            "correo": correo,
            "password": password,
            "rol": rol
        })

        if user_id:
            st.success("Cuenta creada correctamente. Ya puedes iniciar sesión.")
            if st.button("Ir al login"):
                st.session_state["page"] = "login"
                st.experimental_rerun()
        else:
            st.error("Error al crear el usuario")
