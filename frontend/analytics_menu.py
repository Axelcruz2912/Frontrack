import streamlit as st

def analytics_menu():
    #  ESTILOS CSS MEJORADOS
    st.markdown("""
        <style>
        /* Header principal */
        .analytics-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2.5rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.25);
            margin-bottom: 2.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .analytics-header h1 {
            margin: 0;
            font-size: 2.8rem;
            font-weight: 800;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            background: linear-gradient(45deg, #ffffff, #e0e7ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .analytics-header p {
            margin: 0.8rem 0 0 0;
            opacity: 0.95;
            font-size: 1.3rem;
            font-weight: 400;
        }
        
        /* Tarjetas de navegación */
        .nav-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 2rem 1.5rem;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            height: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .nav-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .nav-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
            border-color: #667eea;
        }
        
        .nav-card.disabled {
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            border-color: #cbd5e1;
            opacity: 0.6;
        }
        
        .nav-card.disabled::before {
            background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
        }
        
        .nav-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .nav-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.8rem;
        }
        
        .nav-description {
            font-size: 0.95rem;
            color: #64748b;
            line-height: 1.5;
        }
        
        .nav-badge {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        .nav-badge.admin {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        }
        
        /* Botones */
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        }
        
        .stButton button:disabled {
            background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%) !important;
            transform: none !important;
            box-shadow: none !important;
        }
        
        /* Separador */
        .divider-analytics {
            height: 3px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 2.5rem 0;
            border-radius: 2px;
        }
        
        /* Mensaje de restricción */
        .restriction-message {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 1px solid #f59e0b;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .analytics-header {
                padding: 2rem 1.5rem;
            }
            
            .analytics-header h1 {
                font-size: 2.2rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Obtener información del usuario
    user = st.session_state.get("user", {})
    user_rol = user.get("rol", "empleado")
    es_admin = user_rol == "admin"
    
    # HEADER PRINCIPAL
    st.markdown(f"""
        <div class="analytics-header">
            <h1>📊 Centro de Analytics & IA</h1>
            <p>Inteligencia artificial y análisis predictivo para tu operación</p>
            <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                👤 {user.get('nombre', 'Usuario')} • 🎭 {user_rol.upper()} • 🔐 {'Acceso Completo' if es_admin else 'Acceso Básico'}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    #  TARJETAS DE NAVEGACIÓN
    if not es_admin:
        # VISTA PARA EMPLEADOS - Solo Predictor de Fallas
        st.markdown("""
            <div class="restriction-message">
                <h3 style="margin:0; color: #92400e;">👤 Acceso Limitado</h3>
                <p style="margin:0.5rem 0 0 0; color: #92400e;">
                    Como empleado, tienes acceso al <strong>Predictor de Fallas</strong> para ayudarte en tus tareas diarias.
                    Contacta con un administrador para acceder a más funcionalidades.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Solo mostrar el Predictor de Fallas activo
            if st.button("🔮 Predictor de Fallas", use_container_width=True, key="predictor_fallas"):
                st.session_state["analytics_view"] = "predictor_fallas"
                st.rerun()
            st.caption("Modelos de IA para predecir fallas futuras - ✅ Acceso permitido")
        
        with col2:
            # Botones deshabilitados para empleados
            st.button("📈 Dashboard Principal", use_container_width=True, disabled=True, key="dashboard_disabled")
            st.caption("Vista general con KPIs - ❌ Solo administradores")
        
        col3, col4 = st.columns([1, 1])
        
        with col3:
            st.button("📦 Optimizador de Inventario", use_container_width=True, disabled=True, key="inventario_disabled")
            st.caption("Recomendaciones de stock - ❌ Solo administradores")
        
        with col4:
            st.button("👥 Analytics de Personal", use_container_width=True, disabled=True, key="personal_disabled")
            st.caption("Análisis de rendimiento - ❌ Solo administradores")
    
    else:
        # VISTA PARA ADMINISTRADORES - Acceso completo
        st.markdown("### 🎯 Módulos Disponibles")
        st.markdown("""
            <div style="background: linear-gradient(135deg, #dbeafe 0%, #e0e7ff 100%); padding: 1rem; border-radius: 10px; margin-bottom: 1.5rem;">
                <small>💡 <strong>Administrador detectado:</strong> Tienes acceso completo a todos los módulos de analytics.</small>
            </div>
        """, unsafe_allow_html=True)
        
        # Grid de tarjetas mejorado
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="nav-card">
                    <span class="nav-icon">📈</span>
                    <div class="nav-title">Dashboard Principal</div>
                    <div class="nav-description">Vista general con KPIs y métricas clave del sistema completo</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Acceder al Dashboard", key="dashboard_main", use_container_width=True):
                st.session_state["analytics_view"] = "dashboard_principal"
                st.rerun()
        
        with col2:
            st.markdown("""
                <div class="nav-card">
                    <span class="nav-icon">🔮</span>
                    <div class="nav-title">Predictor de Fallas</div>
                    <div class="nav-description">Modelos avanzados de IA para predecir y prevenir fallas futuras</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Usar Predictor", key="predictor_fallas", use_container_width=True):
                st.session_state["analytics_view"] = "predictor_fallas"
                st.rerun()
        
        with col3:
            st.markdown("""
                <div class="nav-card">
                    <span class="nav-icon">📦</span>
                    <div class="nav-title">Optimizador de Inventario</div>
                    <div class="nav-description">Recomendaciones inteligentes de stock y gestión de materiales</div>
                    <div class="nav-badge admin">ADMIN</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Optimizar Inventario", key="optimizador_inventario", use_container_width=True):
                st.session_state["analytics_view"] = "optimizador_inventario"
                st.rerun()
        
        with col4:
            st.markdown("""
                <div class="nav-card">
                    <span class="nav-icon">👥</span>
                    <div class="nav-title">Analytics de Personal</div>
                    <div class="nav-description">Análisis de rendimiento, asignaciones y gestión del equipo</div>
                    <div class="nav-badge admin">ADMIN</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Analizar Personal", key="analytics_personal", use_container_width=True):
                st.session_state["analytics_view"] = "analytics_personal"
                st.rerun()
    
    #  CONTENIDO PRINCIPAL
    st.markdown('<div class="divider-analytics"></div>', unsafe_allow_html=True)
    
    # Navegación entre vistas
    if "analytics_view" not in st.session_state:
        st.session_state["analytics_view"] = "predictor_fallas" if not es_admin else "dashboard_principal"
    
    # Validar acceso según rol
    vista_actual = st.session_state["analytics_view"]
    vistas_permitidas_empleado = ["predictor_fallas"]
    
    if not es_admin and vista_actual not in vistas_permitidas_empleado:
        st.warning("🚫 **Acceso restringido:** No tienes permisos para ver este módulo. Redirigiendo al Predictor de Fallas...")
        st.session_state["analytics_view"] = "predictor_fallas"
        st.rerun()
    
    # Cargar la vista correspondiente
    try:
        if st.session_state["analytics_view"] == "dashboard_principal" and es_admin:
            from frontend.analytics_views.dashboard_principal import mostrar_dashboard_principal
            mostrar_dashboard_principal()
        
        elif st.session_state["analytics_view"] == "predictor_fallas":
            from frontend.analytics_views.predictor_fallas import mostrar_predictor_fallas
            mostrar_predictor_fallas()
        
        elif st.session_state["analytics_view"] == "optimizador_inventario" and es_admin:
            from frontend.analytics_views.optimizador_inventario import mostrar_optimizador_inventario
            mostrar_optimizador_inventario()
        
        elif st.session_state["analytics_view"] == "analytics_personal" and es_admin:
            from frontend.analytics_views.analytics_personal import mostrar_analytics_personal
            mostrar_analytics_personal()
    
    except Exception as e:
        st.error(f"❌ Error al cargar el módulo: {str(e)}")
        st.info("🔧 Contacta al administrador del sistema para resolver este problema.")