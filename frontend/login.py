import streamlit as st
from backend.models.usuarios import authenticate, create_usuario, correo_existe
import re
import base64
from frontend.recuperar_password import vista_recuperar_password

def get_base64_image(image_path):
    """Convierte una imagen a base64 para embeber en HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f" No se encontró el logo en: {image_path}")
        return None

def login():
    # Cargar logo en base64
    logo_base64 = get_base64_image("img/FontTrack.png")  # Ajusta la ruta según tu estructura
    
    # CSS personalizado con colores Bonafont
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
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        /* Fondo con colores Bonafont */
        .stApp {
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 50%, #00d4ff 100%);
            background-attachment: fixed;
            min-height: 100vh;
        }

        /* Contenedor principal SIN FONDO BLANCO */
        .main-container {
            animation: fadeIn 0.8s ease-out;
            padding-top: 2rem;
            background: transparent !important;
        }

        /* Logo centrado y visible */
        .logo-container {
            text-align: center;
            margin-bottom: 2rem;
            animation: float 3s ease-in-out infinite;
            padding: 0 1rem;
        }

        .logo-container img {
            max-width: 280px;
            height: auto;
            filter: drop-shadow(0 8px 25px rgba(255, 255, 255, 0.3));
            transition: all 0.3s ease;
        }

        .logo-container img:hover {
            transform: scale(1.05);
            filter: drop-shadow(0 12px 30px rgba(255, 255, 255, 0.4));
        }

        /* Subtítulo mejorado */
        .subtitle {
            text-align: center;
            color: #ffffff;
            font-size: 1.3rem;
            font-weight: 500;
            margin-bottom: 3rem;
            animation: slideIn 0.8s ease-out;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }


        /* Sección headers */
        .section-title {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2rem;
            text-align: center;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        /* Inputs mejorados y más visibles */
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

        /* BOTONES MÁS VISIBLES Y ATRACTIVOS */
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

        /* Botón secundario MÁS VISIBLE */
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

        /* Separador elegante */
        .elegant-divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 2.5rem 0;
        }

        .elegant-divider::before,
        .elegant-divider::after {
            content: '';
            flex: 1;
            border-bottom: 2px solid rgba(255, 255, 255, 0.5);
        }

        .elegant-divider span {
            padding: 0 1.5rem;
            color: #ffffff;
            font-weight: 700;
            font-size: 1rem;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        /* Barra de seguridad de contraseña */
        .password-strength {
            margin: 15px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            border-left: 4px solid #ffffff;
            backdrop-filter: blur(10px);
        }

        .strength-bar {
            height: 10px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .strength-fill {
            height: 100%;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .strength-text {
            font-weight: 700;
            font-size: 1rem;
            color: #ffffff;
            text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }

        /* Footer */
        .footer-text {
            text-align: center;
            color: #ffffff;
            padding: 3rem 0 1rem 0;
            font-size: 1rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            margin-top: 3rem;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .logo-container img {
                max-width: 200px;
            }
            .form-container {
                padding: 2rem 1.5rem;
                margin: 0 1rem;
            }
            .subtitle {
                font-size: 1.1rem;
                margin: 0 1rem 2rem 1rem;
            }
            .section-title {
                font-size: 1.6rem;
            }
        }

        /* Ocultar elementos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp > header {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # Inicializar estados
    if "mostrar_registro" not in st.session_state:
        st.session_state["mostrar_registro"] = False
        
    if "mostrar_recuperacion" not in st.session_state:
        st.session_state["mostrar_recuperacion"] = False

    # Contenedor principal SIN FONDO BLANCO
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Logo centrado
    if logo_base64:
        st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" alt="Frontrack Logo">
            </div>
        """, unsafe_allow_html=True)
    
    # Subtítulo con efecto glass
    #st.markdown('<p class="subtitle">Gestiona incidencias y materiales de forma inteligente</p>', unsafe_allow_html=True)

    # Verificar si se debe mostrar la vista de recuperación de contraseña
    if st.session_state.get("pantalla") == "recuperar_password":
        vista_recuperar_password()
        return

    # VISTA LOGIN
    if not st.session_state["mostrar_registro"]:
        col1, col2, col3 = st.columns([0.3, 1.4, 0.3])
        
        with col2:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Iniciar Sesión</h2>', unsafe_allow_html=True)

            correo = st.text_input(
                "📧 Correo Electrónico",
                placeholder="email@bonafont.com",
                help="Ingresa tu correo registrado",
                key="login_correo"
            )

            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="••••••••",
                help="Ingresa tu contraseña",
                key="login_password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 INGRESAR AL SISTEMA", use_container_width=True):
                if not correo or not password:
                    st.error("❌ Por favor completa todos los campos")
                else:
                    with st.spinner("🔐 Verificando credenciales..."):
                        user = authenticate(correo, password)
                        
                        if user:
                            st.session_state["user"] = {
                                "id": str(user["_id"]),
                                "nombre": user["nombre"],
                                "rol": user["rol"],
                                "correo": user["correo"]
                            }
                            st.success(f"🎉 ¡Bienvenido {user['nombre']}!")
                            st.balloons()
                            st.session_state["page"] = "dashboard"
                            st.rerun()
                        else:
                            st.error("❌ Credenciales incorrectas")

            st.markdown('<div class="elegant-divider"><span>O</span></div>', unsafe_allow_html=True)

            # Botones adicionales en columnas
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("📝 CREAR CUENTA", use_container_width=True, type="secondary"):
                    st.session_state["mostrar_registro"] = True
                    st.rerun()
            
            with col_btn2:
                if st.button("🔑 RECUPERAR CONTRASEÑA", use_container_width=True, type="secondary"):
                    st.session_state["pantalla"] = "recuperar_password"
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)  # Cierre del form-container

    # VISTA REGISTRO
    else:
        col1, col2, col3 = st.columns([0.3, 1.4, 0.3])
        
        with col2:
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title">Crear Cuenta</h2>', unsafe_allow_html=True)

            nombre = st.text_input(
                "👤 Nombre Completo",
                placeholder="Juan Pérez González",
                help="Nombre y apellido(s)",
                key="reg_nombre"
            )

            correo = st.text_input(
                "📧 Correo Electrónico",
                placeholder="tu@correo.com",
                help="Correo válido con formato usuario@dominio.com",
                key="reg_correo"
            )

            col_pass1, col_pass2 = st.columns(2)
            
            with col_pass1:
                password = st.text_input(
                    "🔒 Contraseña",
                    type="password",
                    placeholder="••••••••",
                    help="Mínimo 8 caracteres",
                    key="reg_password"
                )
            
            with col_pass2:
                confirmar = st.text_input(
                    "✅ Confirmar Contraseña",
                    type="password",
                    placeholder="••••••••",
                    help="Repite la contraseña",
                    key="reg_confirmar"
                )

            # Indicador de seguridad de contraseña
            if password:
                def evaluar_seguridad(pw):
                    score = 0
                    if len(pw) >= 8: score += 1
                    if any(c.islower() for c in pw): score += 1
                    if any(c.isupper() for c in pw): score += 1
                    if any(c.isdigit() for c in pw): score += 1
                    return score

                level = evaluar_seguridad(password)
                niveles = ["Muy débil", "Débil", "Regular", "Segura"]
                colores = ["#ff4444", "#ffaa00", "#ffdd00", "#00ff00"]
                pct = max(15, int((level/4)*100))

                st.markdown(f"""
                    <div class="password-strength">
                        <div class="strength-bar">
                            <div class="strength-fill" style="width:{pct}%; background:{colores[level-1] if level > 0 else '#ff4444'};"></div>
                        </div>
                        <div class="strength-text" style="color:{colores[level-1] if level > 0 else '#ff4444'};">
                            🔐 Seguridad: {niveles[level-1] if level > 0 else niveles[0]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🚀 CREAR MI CUENTA", use_container_width=True):
                # Validaciones
                if not nombre or not correo or not password or not confirmar:
                    st.error("❌ Todos los campos son obligatorios")
                    st.stop()

                # Validar nombre (mínimo 2 palabras, solo letras)
                tokens = [t for t in nombre.strip().split() if t]
                if len(tokens) < 2:
                    st.warning("⚠️ Ingresa nombre completo (nombre y apellido)")
                    st.stop()
                
                if not all(token.replace(" ", "").isalpha() for token in tokens):
                    st.warning("⚠️ El nombre solo debe contener letras")
                    st.stop()

                # Validar correo con regex robusto
                email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                if not re.match(email_pattern, correo):
                    st.warning("⚠️ Formato de correo inválido")
                    st.stop()

                # Verificar si el correo ya existe
                if correo_existe(correo):
                    st.error("❌ Este correo ya está registrado")
                    st.stop()

                # Validar contraseña (mínimo 8 caracteres)
                if len(password) < 8:
                    st.warning("⚠️ La contraseña debe tener mínimo 8 caracteres")
                    st.stop()

                if not any(c.islower() for c in password):
                    st.warning("⚠️ Incluye al menos una minúscula")
                    st.stop()

                if not any(c.isupper() for c in password):
                    st.warning("⚠️ Incluye al menos una mayúscula")
                    st.stop()

                if not any(c.isdigit() for c in password):
                    st.warning("⚠️ Incluye al menos un número")
                    st.stop()

                # Verificar que las contraseñas coincidan
                if password != confirmar:
                    st.error("❌ Las contraseñas no coinciden")
                    st.stop()

                # Crear usuario
                with st.spinner("⏳ Creando tu cuenta..."):
                    try:
                        create_usuario(
                            nombre=nombre.strip(),
                            correo=correo.strip().lower(),
                            rol="empleado",
                            password=password
                        )
                        st.success("🎉 ¡Cuenta creada exitosamente!")
                        st.balloons()
                        st.info("✅ Ya puedes iniciar sesión")
                        st.session_state["mostrar_registro"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error al crear la cuenta: {e}")
                        st.stop()

            st.markdown('<div class="elegant-divider"><span></span></div>', unsafe_allow_html=True)

            if st.button("← VOLVER AL LOGIN", use_container_width=True, type="secondary"):
                st.session_state["mostrar_registro"] = False
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)  # Cierre del form-container

    st.markdown('</div>', unsafe_allow_html=True)  # Cierre del main-container

    # Footer
    st.markdown("""
        <div class="footer-text">
            <p>🔒 Tus datos están protegidos con encriptación de nivel empresarial</p>
        </div>
    """, unsafe_allow_html=True)