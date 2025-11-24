import streamlit as st
from datetime import datetime

def perfil_usuario():
    # Verificar sesión
    if "user" not in st.session_state:
        st.error("⚠️ Sesión no válida. Redirigiendo al login...")
        st.session_state["page"] = "login"
        st.rerun()

    usuario = st.session_state["user"]

    st.markdown("""
        <style>
        /* Animaciones sofisticadas */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
        }

        @keyframes shimmer {
            0% {
                background-position: -1000px 0;
            }
            100% {
                background-position: 1000px 0;
            }
        }

        /* Fondo con gradiente Bonafont */
        .stApp {
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 50%, #00d4ff 100%);
            background-attachment: fixed;
        }

        /* Contenedor principal */
        .profile-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        /* Header del perfil con avatar */
        .profile-header {
            background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.98) 100%);
            backdrop-filter: blur(20px);
            padding: 3rem 2.5rem;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 102, 204, 0.3);
            text-align: center;
            animation: fadeInUp 0.6s ease-out;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }

        .profile-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 3s infinite;
        }

        /* Avatar circular */
        .avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1.5rem;
            font-size: 3.5rem;
            box-shadow: 0 10px 30px rgba(0, 102, 204, 0.4);
            animation: scaleIn 0.8s ease-out;
            position: relative;
            z-index: 1;
        }

        .avatar:hover {
            animation: pulse 0.6s ease-in-out;
        }

        /* Nombre del usuario */
        .user-name {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
            animation: slideInLeft 0.8s ease-out;
            position: relative;
            z-index: 1;
        }

        .user-role {
            display: inline-block;
            background: linear-gradient(135deg, #0066cc 0%, #00a8e8 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
            animation: slideInLeft 1s ease-out;
            position: relative;
            z-index: 1;
        }

        /* Cards de información */
        .info-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 102, 204, 0.2);
            margin-bottom: 1.5rem;
            animation: fadeInUp 0.8s ease-out;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }

        .info-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0, 102, 204, 0.3);
        }

        .info-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #0066cc;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .info-item {
            display: flex;
            align-items: center;
            padding: 1rem;
            margin-bottom: 0.75rem;
            background: #f8f9fa;
            border-radius: 12px;
            border-left: 4px solid #0066cc;
            transition: all 0.3s ease;
            animation: slideInLeft 1s ease-out;
        }

        .info-item:hover {
            background: #e3f2fd;
            transform: translateX(5px);
        }

        .info-label {
            font-weight: 600;
            color: #0066cc;
            min-width: 100px;
            font-size: 0.95rem;
        }

        .info-value {
            color: #333;
            font-size: 1rem;
            flex: 1;
        }

        /* Botón de cerrar sesión mejorado */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px;
            padding: 16px 28px;
            font-size: 1.1rem;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 8px 24px rgba(220, 53, 69, 0.35);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(220, 53, 69, 0.5);
            background: linear-gradient(135deg, #c82333 0%, #bd2130 100%) !important;
        }

        /* Stats cards */
        .stats-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            box-shadow: 0 8px 24px rgba(0, 102, 204, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: scaleIn 1s ease-out;
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 32px rgba(0, 102, 204, 0.3);
        }

        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #0066cc;
            margin-bottom: 0.25rem;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #6c757d;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Divider decorativo */
        .divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #0066cc, transparent);
            margin: 2rem 0;
            animation: shimmer 3s infinite;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .profile-header {
                padding: 2rem 1.5rem;
            }
            
            .user-name {
                font-size: 1.6rem;
            }

            .avatar {
                width: 100px;
                height: 100px;
                font-size: 2.5rem;
            }

            .stats-container {
                grid-template-columns: 1fr;
            }
        }

        /* Ocultar elementos de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="profile-container">', unsafe_allow_html=True)

    # Header con avatar y nombre
    st.markdown(f"""
        <div class="profile-header">
            <div class="avatar">
                {usuario['nombre'][0].upper()}
            </div>
            <h1 class="user-name">{usuario['nombre']}</h1>
            <span class="user-role">🏷️ {usuario['rol'].capitalize()}</span>
        </div>
    """, unsafe_allow_html=True)



    # Información detallada del usuario
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="info-card">
                <div class="info-title">
                    👤 Información Personal
                </div>
                <div class="info-item">
                    <span class="info-label">📧 Correo:</span>
                    <span class="info-value">{}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">🆔 ID Usuario:</span>
                    <span class="info-value">{}</span>
                </div>
            </div>
        """.format(usuario['correo'], usuario['id'][:8] + "..."), unsafe_allow_html=True)

    with col2:
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        hora_actual = datetime.now().strftime("%H:%M")
        
        st.markdown(f"""
            <div class="info-card">
                <div class="info-title">
                    🕐 Información de Sesión
                </div>
                <div class="info-item">
                    <span class="info-label">📅 Fecha:</span>
                    <span class="info-value">{fecha_actual}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">⏰ Hora:</span>
                    <span class="info-value">{hora_actual}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Divider decorativo
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Botón de cerrar sesión
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚪 CERRAR SESIÓN", key="logout", help="Salir de tu cuenta"):
            with st.spinner("👋 Cerrando sesión..."):
                st.session_state.clear()
                st.success("✅ Sesión cerrada correctamente")
                st.session_state["page"] = "login"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer informativo
    st.markdown("""
        <div style="text-align: center; color: white; padding: 2rem 0; margin-top: 2rem;">
            <p style="font-size: 0.95rem; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
                🔒 Tu sesión está protegida y encriptada
            </p>
        </div>
    """, unsafe_allow_html=True)