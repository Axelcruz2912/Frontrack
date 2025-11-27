import streamlit as st
from backend.controllers.auth_controller import solicitar_reset

def vista_recuperar_password():
    st.title("Recuperar contraseña")

    st.write("Ingresa tu correo para enviarte un enlace de recuperación.")

    correo = st.text_input("Correo registrado")

    if st.button("Enviar enlace"):
        enviado = solicitar_reset(correo)

        if enviado:
            st.success("Se ha enviado un enlace de recuperación a tu correo.")
        else:
            st.error("Ese correo no está registrado.")

    if st.button("Volver al login"):
        st.session_state["pantalla"] = "login"
