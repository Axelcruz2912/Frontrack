import streamlit as st
from backend.controllers.auth_controller import confirmar_reset
import time

def reset_password_view():
    # CSS personalizado con el mismo estilo
    st.markdown("""
        <style>
        /* Animaciones */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }

        /* Fondo con colores Bonafont */
        .stApp {
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 50%, #00d4ff 100%);
            background-attachment: fixed;
            min-height: 100vh;
        }

        /* Contenedor principal */
        .main-container {
            animation: fadeIn 0.8s ease-out;
            padding-top: 3rem;
            background: transparent !important;
        }

        /* Contenedor de formulario */
        .form-container {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            padding: 3rem 2.5rem;
            border-radius: 24px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            max-width: 480px;
            margin: 0 auto;
            box-shadow: 0 20px 60px rgba(0, 102, 204, 0.4);
        }

        /* Títulos */
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 1rem;
            text-align: center;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .section-subtitle {
            font-size: 1.1rem;
            color: #ffffff;
            margin-bottom: 2rem;
            text-align: center;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        /* Inputs mejorados */
        .stTextInput > div > div > input {
            border-radius: 15px;
            border: 2px solid rgba(255, 255, 255, 0.5);
            padding: 16px 20px;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-weight: 500;
        }

        .stTextInput > div > div > input:focus {
            border-color: #ffffff;
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            background: white;
        }

        .stTextInput > label {
            font-weight: 700;
            color: #ffffff;
            font-size: 1rem;
            margin-bottom: 8px;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        /* Botones principales */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 100%) !important;
            color: #0066cc !important;
            border: 3px solid #ffffff !important;
            border-radius: 15px;
            padding: 18px 32px;
            font-size: 1.2rem;
            font-weight: 800;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(255, 255, 255, 0.4);
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton > button:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 255, 255, 0.6);
            background: linear-gradient(135deg, #ffffff 0%, #ffffff 100%) !important;
            color: #0066cc !important;
            border-color: #ffffff !important;
        }

        /* Botón secundario */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 3px solid #ffffff !important;
            color: #ffffff !important;
            box-shadow: 0 8px 25px rgba(255, 255, 255, 0.3) !important;
            font-weight: 700;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #ffffff !important;
            color: #0066cc !important;
            box-shadow: 0 12px 35px rgba(255, 255, 255, 0.5) !important;
            transform: translateY(-3px);
        }

        /* Mensajes de alerta */
        .stAlert {
            border-radius: 15px;
            animation: slideIn 0.5s ease-out;
            border: none;
            backdrop-filter: blur(10px);
        }

        /* Enlaces personalizados */
        .custom-link {
            display: block;
            text-align: center;
            color: #ffffff !important;
            font-weight: 600;
            text-decoration: none;
            padding: 12px 24px;
            margin: 10px 0;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        .custom-link:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
            text-decoration: none;
            color: #ffffff !important;
        }

        /* Ocultar elementos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp > header {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # Contenedor principal
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.3, 1.4, 0.3])
    
    with col2:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Obtener token desde la URL de forma segura
        token = st.query_params.get("token", None)

        if not token:
            st.markdown('<h2 class="section-title">❌ Token Inválido</h2>', unsafe_allow_html=True)
            st.markdown('<p class="section-subtitle">El enlace de recuperación es inválido o ha expirado</p>', unsafe_allow_html=True)
            
            # Usar botón en lugar de markdown para mejor funcionalidad
            if st.button("🔙 VOLVER AL INICIO", use_container_width=True, type="secondary"):
                st.session_state["page"] = "login"
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            return

        st.markdown('<h2 class="section-title">🔐 Restablecer Contraseña</h2>', unsafe_allow_html=True)
        st.markdown('<p class="section-subtitle">Ingresa tu nueva contraseña para continuar</p>', unsafe_allow_html=True)

        nueva_contra = st.text_input(
            "🔒 Nueva contraseña", 
            type="password",
            placeholder="••••••••",
            help="Mínimo 8 caracteres, con mayúsculas, minúsculas y números"
        )
        
        confirmar = st.text_input(
            "✅ Confirmar contraseña", 
            type="password",
            placeholder="••••••••",
            help="Repite la misma contraseña"
        )

        if st.button("🚀 ACTUALIZAR CONTRASEÑA", use_container_width=True):
            if not nueva_contra or not confirmar:
                st.warning("⚠️ Debes llenar ambos campos")
                return

            if nueva_contra != confirmar:
                st.error("❌ Las contraseñas no coinciden")
                return

            # Validar fortaleza de contraseña
            if len(nueva_contra) < 8:
                st.warning("⚠️ La contraseña debe tener mínimo 8 caracteres")
                return

            if not any(c.islower() for c in nueva_contra):
                st.warning("⚠️ Incluye al menos una minúscula")
                return

            if not any(c.isupper() for c in nueva_contra):
                st.warning("⚠️ Incluye al menos una mayúscula")
                return

            if not any(c.isdigit() for c in nueva_contra):
                st.warning("⚠️ Incluye al menos un número")
                return

            with st.spinner("🔄 Actualizando contraseña..."):
                resultado = confirmar_reset(token, nueva_contra)

            if resultado:
                st.success("🎉 ¡Contraseña actualizada correctamente!")
                st.balloons()
                
                # Limpiar parámetros para evitar volver a abrir esta vista
                st.query_params.clear()
                
                # Redirección automática después de 3 segundos
                st.info("⏳ Redirigiendo al login en 3 segundos...")
                time.sleep(3)
                
                # Redirigir automáticamente al login
                st.session_state["page"] = "login"
                st.rerun()

            else:
                st.error("❌ El token expiró o es inválido")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🔄 SOLICITAR NUEVO ENLACE", use_container_width=True, type="secondary"):
                        st.session_state["page"] = "forgot_password"
                        st.rerun()
                with col_btn2:
                    if st.button("🔙 VOLVER AL LOGIN", use_container_width=True, type="secondary"):
                        st.session_state["page"] = "login"
                        st.rerun()

        # Botones adicionales cuando no se ha enviado el formulario
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔙 CANCELAR", use_container_width=True, type="secondary"):
                    st.session_state["page"] = "login"
                    st.rerun()
            with col_btn2:
                if st.button("🔄 NUEVO ENLACE", use_container_width=True, type="secondary"):
                    st.session_state["page"] = "forgot_password"
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # Cierre del form-container
    
    st.markdown('</div>', unsafe_allow_html=True)  # Cierre del main-container