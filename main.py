import streamlit as st
from frontend.login import login
from frontend.dashboard_admin import admin_dashboard
from frontend.dashboard_empleado import empleado_dashboard
from frontend.perfil_usuariooo import perfil_usuario
from frontend.crud_menu import crud_menu
from frontend.analytics_menu import analytics_menu
from frontend.reset_password import reset_password_view


# 🎨 ESTILOS CSS MEJORADOS
st.markdown("""
    <style>
    /* Estilos globales */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        color: white;
    }
    
    /* User info card */
    .user-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        margin-bottom: 1.5rem;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .user-name {
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0.5rem 0;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    
    .user-email {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.3rem 0;
    }
    
    .user-role {
        background: rgba(255, 255, 255, 0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
        display: inline-block;
    }
    
    /* Navigation radio buttons */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    /* Radio button styling */
    .st-eb, .st-ec {
        background: transparent !important;
    }
    
    div[data-testid="stRadio"] label {
        color: white !important;
        font-weight: 500;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stRadio"] label:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateX(5px);
    }
    
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Logout button */
    .logout-btn {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
        transition: all 0.3s ease !important;
    }
    
    .logout-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* Separator */
    .sidebar-separator {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 1.5rem 0;
    }
    
    /* Main content area */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        margin-bottom: 2rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .user-card {
            padding: 1rem;
        }
        
        .user-name {
            font-size: 1.1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)
query_params = st.query_params

# 1️⃣ Si viene un token en la URL → forzar pantalla de reset password
if "token" in query_params:
    from frontend.reset_password import reset_password_view
    reset_password_view()
    st.stop()

# 2️⃣ Estado inicial (solo si no hay token)
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# 3️⃣ Si no está logueado → mostrar login
# (Esto se ejecuta solo si no hay token)
if st.session_state["page"] == "login":
    login()
    st.stop()

# 4️⃣ Si sí está logueado → validar usuario y mostrar menú
user = st.session_state.get("user", None)

if not user:
    st.session_state["page"] = "login"
    st.rerun()

# -------- SIDEBAR MEJORADO --------
with st.sidebar:
    # 🎯 TARJETA DE USUARIO MEJORADA
    st.markdown(f"""
        <div class="user-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{"👑" if user["rol"] == "admin" else "👤"}</div>
            <div class="user-name">{user['nombre']}</div>
            <div class="user-email">📧 {user['correo']}</div>
            <div class="user-role">{user['rol'].upper()}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 📋 OPCIONES DE NAVEGACIÓN MEJORADAS
    st.markdown("### 🧭 Navegación")
    
    # Definir opciones según rol con emojis y descripciones
    if user["rol"] == "admin":
        opciones_data = [
            {"icon": "📊", "label": "Dashboard", "desc": "Vista general del sistema"},
            {"icon": "👤", "label": "Perfil", "desc": "Gestiona tu cuenta"},
            {"icon": "🔧", "label": "CRUD", "desc": "Gestión de datos"},
            {"icon": "📈", "label": "Analytics & IA", "desc": "Análisis avanzado"}
        ]
    else:
        opciones_data = [
            {"icon": "📊", "label": "Dashboard", "desc": "Tu vista personal"},
            {"icon": "👤", "label": "Perfil", "desc": "Gestiona tu cuenta"},
            {"icon": "🔧", "label": "CRUD", "desc": "Operaciones básicas"},
            {"icon": "📈", "label": "Analytics & IA", "desc": "Estadísticas"}
        ]
    
    # Crear opciones para el radio button
    opciones = [f"{item['icon']} {item['label']}" for item in opciones_data]
    
    # Radio button mejorado
    opcion = st.radio(
        "Selecciona una opción:",
        opciones,
        key="main_navigation"
    )
    
    # Mostrar descripción de la opción seleccionada
    opcion_seleccionada = next((item for item in opciones_data if item['icon'] + " " + item['label'] == opcion), None)
    if opcion_seleccionada:
        st.markdown(f"""
            <div style="background: rgba(255,255,255,0.1); padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #667eea;">
                <small>💡 {opcion_seleccionada['desc']}</small>
            </div>
        """, unsafe_allow_html=True)
    
    # Separador
    st.markdown('<div class="sidebar-separator"></div>', unsafe_allow_html=True)
    
    # ℹ️ INFORMACIÓN DEL SISTEMA
    st.markdown("### ℹ️ Sistema")
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <div style="font-size: 0.8rem; opacity: 0.8;">
                <div>🟢 <strong>Conectado</strong></div>
                <div>👥 Rol: <strong>{user['rol'].capitalize()}</strong></div>
                <div>🔐 Permisos: <strong>{"Completos" if user["rol"] == "admin" else "Básicos"}</strong></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # 🚪 BOTÓN DE LOGOUT MEJORADO
    st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.8rem !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stButton"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("🚪 Cerrar Sesión", use_container_width=True, key="logout_btn"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state["page"] = "login"
        st.rerun()

# -------- MAPPING DE NAVEGACIÓN --------
navigation_map = {
    "📊 Dashboard": "dashboard",
    "👤 Perfil": "perfil", 
    "🔧 CRUD": "crud_menu",
    "📈 Analytics & IA": "analytics"
}

# Actualizar página según selección
st.session_state["page"] = navigation_map.get(opcion, "dashboard")

# -------- CONTENIDO PRINCIPAL CON HEADER MEJORADO --------
page_titles = {
    "dashboard": "📊 Dashboard Principal",
    "perfil": "👤 Perfil de Usuario", 
    "crud_menu": "🔧 Gestión de Datos",
    "analytics": "📈 Analytics & Inteligencia Artificial"
}

# Header de página
current_page_title = page_titles.get(st.session_state["page"], "Sistema de Gestión")
st.markdown(f"""
    <div class="main-header">
        <h1 style="margin:0; font-size: 2.5rem; font-weight: 700;">{current_page_title}</h1>
        <p style="margin:0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">
            Bienvenido de vuelta, {user['nombre']}
        </p>
    </div>
""", unsafe_allow_html=True)

# -------- ROUTING DE PÁGINAS --------
if st.session_state["page"] == "dashboard":
    if user["rol"] == "admin":
        admin_dashboard()
    else:
        empleado_dashboard()

elif st.session_state["page"] == "perfil":
    perfil_usuario()

elif st.session_state["page"] == "crud_menu":
    crud_menu()

elif st.session_state["page"] == "analytics":
    analytics_menu()