import streamlit as st
from backend.models.usuarios import authenticate, create_usuario, correo_existe
import re
import base64

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
        }

        /* Contenedor principal */
        .main-container {
            animation: fadeIn 0.8s ease-out;
            padding-top: 2rem;
        }

        /* Tarjeta de login con efecto glassmorphism */
        .login-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 3rem 2.5rem;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 102, 204, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.3);
            max-width: 480px;
            margin: 0 auto;
        }

        /* Contenedor del logo */
        .logo-container {
            text-align: center;
            margin-bottom: 1.5rem;
            animation: float 3s ease-in-out infinite;
        }

        .logo-container img {
            max-width: 180px;
            height: auto;
            filter: drop-shadow(0 4px 12px rgba(0, 102, 204, 0.2));
            transition: all 0.3s ease;
        }

        .logo-container img:hover {
            transform: scale(1.05);
            filter: drop-shadow(0 6px 16px rgba(0, 102, 204, 0.3));
        }

        /* Logo/Título principal */
        .main-title {
            font-size: 3.2rem;
            font-weight: 900;
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 0.5rem;
            animation: slideIn 0.6s ease-out;
            letter-spacing: -1px;
        }

        .subtitle {
            text-align: center;
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 2.5rem;
            animation: slideIn 0.8s ease-out;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Sección headers */
        .section-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #0066cc;
            margin-bottom: 1.5rem;
            text-align: center;
        }

        /* Inputs mejorados */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 2px solid #e3f2fd;
            padding: 14px 18px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: #fafbfc;
        }

        .stTextInput > div > div > input:focus {
            border-color: #0066cc;
            box-shadow: 0 0 0 4px rgba(0, 102, 204, 0.1);
            transform: translateY(-2px);
            background: white;
        }

        .stTextInput > label {
            font-weight: 600;
            color: #1a1a1a;
            font-size: 0.95rem;
        }

        /* Botones mejorados */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px;
            padding: 16px 28px;
            font-size: 1.1rem;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(0, 102, 204, 0.35);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(0, 102, 204, 0.5);
            animation: pulse 0.6s ease-in-out;
        }

        /* Botón secundario */
        .stButton > button[kind="secondary"] {
            background: transparent !important;
            border: 2px solid #0066cc !important;
            color: #0066cc !important;
            box-shadow: none !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #0066cc !important;
            color: white !important;
            box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3) !important;
        }

        /* Mensajes de alerta */
        .stAlert {
            border-radius: 12px;
            animation: slideIn 0.5s ease-out;
            border: none;
        }

        /* Separador elegante */
        .elegant-divider {
            display: flex;
            align-items: center;
            text-align: center;
            margin: 2rem 0;
        }

        .elegant-divider::before,
        .elegant-divider::after {
            content: '';
            flex: 1;
            border-bottom: 2px solid #e3f2fd;
        }

        .elegant-divider span {
            padding: 0 1rem;
            color: #0066cc;
            font-weight: 700;
            font-size: 0.9rem;
        }

        /* Barra de seguridad de contraseña */
        .password-strength {
            margin: 12px 0;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #0066cc;
        }

        .strength-bar {
            height: 8px;
            background: #e9ecef;
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 8px;
        }

        .strength-fill {
            height: 100%;
            border-radius: 6px;
            transition: all 0.3s ease;
        }

        .strength-text {
            font-weight: 600;
            font-size: 0.9rem;
        }

        /* Ícono flotante */
        .icon-float {
            animation: float 3s ease-in-out infinite;
            display: inline-block;
        }

        /* Footer */
        .footer-text {
            text-align: center;
            color: #ffffff;
            padding: 2rem 0;
            font-size: 0.95rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Responsive */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.2rem;
            }
            .login-card {
                padding: 2rem 1.5rem;
            }
            .subtitle {
                font-size: 1rem;
            }
            .logo-container img {
                max-width: 140px;
            }
        }

        /* Ocultar elementos de Streamlit */
        
        </style>
    """, unsafe_allow_html=True)

    
    # Inicializar estados
    if "mostrar_registro" not in st.session_state:
        st.session_state["mostrar_registro"] = False

    # Contenedor principal
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    
    # Título y subtítulo
    # Logo embebido en base64
    if logo_base64:
        st.markdown(f"""
            <div class="logo-container">
                <img src="data:image/png;base64,{logo_base64}" alt="Frontrack Logo">
            </div>
        """, unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Gestiona incidencias y materiales de forma inteligente</p>', unsafe_allow_html=True)

    # VISTA LOGIN
    if not st.session_state["mostrar_registro"]:
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        
        with col2:
            st.markdown('<h2 class="section-title"> Iniciar Sesión</h2>', unsafe_allow_html=True)

            correo = st.text_input(
                " Correo Electrónico",
                placeholder="email@bonafont.com",
                help="Ingresa tu correo registrado",
                key="login_correo"
            )

            password = st.text_input(
                " Contraseña",
                type="password",
                placeholder="••••••••",
                help="Ingresa tu contraseña",
                key="login_password"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(" INGRESAR", use_container_width=True):
                if not correo or not password:
                    st.error(" Por favor completa todos los campos")
                else:
                    with st.spinner(" Verificando credenciales..."):
                        user = authenticate(correo, password)
                        
                        if user:
                            st.session_state["user"] = {
                                "id": str(user["_id"]),
                                "nombre": user["nombre"],
                                "rol": user["rol"],
                                "correo": user["correo"]
                            }
                            st.success(f" ¡Bienvenido {user['nombre']}! ")
                            st.balloons()
                            st.session_state["page"] = "dashboard"
                            st.rerun()
                        else:
                            st.error(" Credenciales incorrectas")

            st.markdown('<div class="elegant-divider"><span>O</span></div>', unsafe_allow_html=True)

            if st.button(" CREAR CUENTA NUEVA", use_container_width=True, type="secondary"):
                st.session_state["mostrar_registro"] = True
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    # VISTA REGISTRO
    else:
        col1, col2, col3 = st.columns([0.5, 2, 0.5])
        
        with col2:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.markdown('<h2 class="section-title"> Crear Cuenta</h2>', unsafe_allow_html=True)

            nombre = st.text_input(
                " Nombre Completo",
                placeholder="Juan Pérez González",
                help="Nombre y apellido(s)",
                key="reg_nombre"
            )

            correo = st.text_input(
                " Correo Electrónico",
                placeholder="tu@correo.com",
                help="Correo válido con formato usuario@dominio.com",
                key="reg_correo"
            )

            col_pass1, col_pass2 = st.columns(2)
            
            with col_pass1:
                password = st.text_input(
                    " Contraseña",
                    type="password",
                    placeholder="••••••••",
                    help="Mínimo 8 caracteres",
                    key="reg_password"
                )
            
            with col_pass2:
                confirmar = st.text_input(
                    " Confirmar",
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
                colores = ["#dc3545", "#fd7e14", "#ffc107", "#198754"]
                pct = max(15, int((level/4)*100))

                st.markdown(f"""
                    <div class="password-strength">
                        <div class="strength-bar">
                            <div class="strength-fill" style="width:{pct}%; background:{colores[level-1] if level > 0 else '#dc3545'};"></div>
                        </div>
                        <div class="strength-text" style="color:{colores[level-1] if level > 0 else '#dc3545'};">
                            Seguridad: {niveles[level-1] if level > 0 else niveles[0]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(" REGISTRAR CUENTA", use_container_width=True):
                # Validaciones
                if not nombre or not correo or not password or not confirmar:
                    st.error(" Todos los campos son obligatorios")
                    st.stop()

                # Validar nombre (mínimo 2 palabras, solo letras)
                tokens = [t for t in nombre.strip().split() if t]
                if len(tokens) < 2:
                    st.warning(" Ingresa nombre completo (nombre y apellido)")
                    st.stop()
                
                if not all(token.replace(" ", "").isalpha() for token in tokens):
                    st.warning(" El nombre solo debe contener letras")
                    st.stop()

                # Validar correo con regex robusto
                email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
                if not re.match(email_pattern, correo):
                    st.warning(" Formato de correo inválido")
                    st.stop()

                # Verificar si el correo ya existe
                if correo_existe(correo):
                    st.error(" Este correo ya está registrado")
                    st.stop()

                # Validar contraseña (mínimo 8 caracteres)
                if len(password) < 8:
                    st.warning(" La contraseña debe tener mínimo 8 caracteres")
                    st.stop()

                if not any(c.islower() for c in password):
                    st.warning(" Incluye al menos una minúscula")
                    st.stop()

                if not any(c.isupper() for c in password):
                    st.warning(" Incluye al menos una mayúscula")
                    st.stop()

                if not any(c.isdigit() for c in password):
                    st.warning(" Incluye al menos un número")
                    st.stop()

                # Verificar que las contraseñas coincidan
                if password != confirmar:
                    st.error(" Las contraseñas no coinciden")
                    st.stop()

                # Crear usuario
                with st.spinner(" Creando tu cuenta..."):
                    try:
                        create_usuario(
                            nombre=nombre.strip(),
                            correo=correo.strip().lower(),
                            rol="empleado",
                            password=password
                        )
                        st.success(" ¡Cuenta creada exitosamente!")
                        st.balloons()
                        st.info(" Ya puedes iniciar sesión")
                        st.session_state["mostrar_registro"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f" Error al crear la cuenta: {e}")
                        st.stop()

            st.markdown('<div class="elegant-divider"><span></span></div>', unsafe_allow_html=True)

            if st.button("← VOLVER AL LOGIN", use_container_width=True, type="secondary"):
                st.session_state["mostrar_registro"] = False
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer-text">
            <p> Tus datos están protegidos con encriptación de nivel empresarial</p>
        </div>
    """, unsafe_allow_html=True)