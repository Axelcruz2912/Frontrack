from backend.models.usuarios import (
    create_reset_token,
    reset_password
)
from backend.utils.email import enviar_correo


# 1️Solicitar recuperación

def solicitar_reset(correo):
    token = create_reset_token(correo)

    if not token:
        return False

    enlace = f"http://localhost:8501/reset_password?token={token}"

    mensaje = f"""
    <h3>Recuperación de contraseña</h3>
    <p>Haz clic en el siguiente enlace para restablecer tu contraseña:</p>
    <a href="{enlace}">Restablecer contraseña</a>
    """

    enviar_correo(correo, "Recuperación de contraseña", mensaje)
    return True


# 2️ Confirmar recuperación

def confirmar_reset(token, nueva_contra):
    """Recibe el token y actualiza la contraseña"""
    return reset_password(token, nueva_contra)
