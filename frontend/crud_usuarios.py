import streamlit as st
from backend.controllers.usuarios_controller import (
    get_all_usuarios,
    get_usuarios_paginados,
    buscar_usuarios,
    create_usuario_controller,
    update_usuario,
    delete_usuario
)


def crud_usuarios():
    #  ESTILOS CSS PERSONALIZADOS
    st.markdown("""
        <style>
        /* Estilos globales */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header principal */
        .header-principal {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-principal h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .header-principal p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }
        
        /* Cards de usuario */
        .usuario-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .usuario-card:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        /* Badges de rol */
        .badge-admin {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .badge-empleado {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }
        
        /* Sección de búsqueda */
        .search-section {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
        }
        
        /* Información de paginación */
        .pagination-info {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            margin: 1rem 0;
        }
        
        /* Separadores */
        .custom-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 1.5rem 0;
        }
        
        /* Formulario de creación */
        .form-container {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        }
        
        /* Botones personalizados */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        /* Info boxes */
        .info-box {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Stats cards */
        .stat-card {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # HEADER PRINCIPAL
    st.markdown("""
        <div class="header-principal">
            <h1>👥 Gestión de Usuarios</h1>
            <p>Administra usuarios de manera eficiente y profesional</p>
        </div>
    """, unsafe_allow_html=True)
    
    #  INICIALIZAR ESTADO PARA MENSAJES
    if "mensaje" not in st.session_state:
        st.session_state.mensaje = None
    if "tipo_mensaje" not in st.session_state:
        st.session_state.tipo_mensaje = None
    
    #  MOSTRAR MENSAJES EXISTENTES
    if st.session_state.mensaje:
        if st.session_state.tipo_mensaje == "success":
            st.success(f"✅ {st.session_state.mensaje}")
        elif st.session_state.tipo_mensaje == "error":
            st.error(f"❌ {st.session_state.mensaje}")
        elif st.session_state.tipo_mensaje == "warning":
            st.warning(f"⚠️ {st.session_state.mensaje}")
        elif st.session_state.tipo_mensaje == "info":
            st.info(f"ℹ️ {st.session_state.mensaje}")
        
        st.session_state.mensaje = None
        st.session_state.tipo_mensaje = None

    tab1, tab2 = st.tabs(["➕ Crear Usuario", "📋 Gestionar Usuarios"])

    #  CREAR USUARIO
    with tab1:
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("### ✨ Registrar nuevo usuario")
        st.markdown("Completa el formulario para agregar un nuevo usuario al sistema.")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input(
                "👤 Nombre completo",
                placeholder="Ej: Juan Pérez García",
                help="Introduce el nombre tal como debe aparecer en el sistema."
            )
            
            correo = st.text_input(
                "📧 Correo electrónico",
                placeholder="usuario@ejemplo.com",
                help="Debe ser válido. El sistema verificará si ya existe."
            )
        
        with col2:
            rol = st.selectbox(
                "🎭 Rol del usuario",
                ["empleado", "admin"],
                help="Elige el nivel de acceso.",
                key="create_role_selectbox"
            )
            
            password = st.text_input(
                "🔒 Contraseña",
                type="password",
                placeholder="Mínimo 6 caracteres",
                help="Debe tener al menos 6 caracteres."
            )

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("✨ Crear usuario", type="primary", use_container_width=True):
                if not nombre or not correo or not password:
                    st.session_state.mensaje = "Todos los campos son obligatorios."
                    st.session_state.tipo_mensaje = "warning"
                    st.rerun()

                if len(password) < 6:
                    st.session_state.mensaje = "La contraseña debe tener al menos 6 caracteres."
                    st.session_state.tipo_mensaje = "warning"
                    st.rerun()

                resultado = create_usuario_controller(nombre, correo, rol, password)

                if "error" in resultado:
                    st.session_state.mensaje = resultado["error"]
                    st.session_state.tipo_mensaje = "error"
                    st.rerun()
                else:
                    st.session_state.mensaje = "Usuario creado exitosamente."
                    st.session_state.tipo_mensaje = "success"
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    #   LISTAR / EDITAR / ELIMINAR
    with tab2:
        #  SECCIÓN DE BÚSQUEDA Y FILTROS
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 Búsqueda y Filtros")
        
        # Búsqueda rápida destacada
        busqueda_rapida = st.text_input(
            "⚡ Búsqueda rápida",
            placeholder="🔎 Busca por nombre o correo...",
            key="busqueda_rapida",
            label_visibility="collapsed"
        )
        
        with st.expander("🎛️ Filtros avanzados", expanded=False):
            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                filtro_nombre = st.text_input(
                    "👤 Nombre",
                    placeholder="Filtrar por nombre",
                    key="filtro_nombre"
                )
            
            with col_filtro2:
                filtro_correo = st.text_input(
                    "📧 Correo",
                    placeholder="Filtrar por correo",
                    key="filtro_correo"
                )
            
            with col_filtro3:
                filtro_rol = st.selectbox(
                    "🎭 Rol",
                    ["", "admin", "empleado"],
                    key="filtro_rol"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        #  CONFIGURACIÓN DE PAGINACIÓN
        col_config1, col_config2, col_config3, col_config4 = st.columns([1, 1, 1, 1])
        
        with col_config1:
            por_pagina = st.selectbox(
                "📄 Por página",
                [5, 10, 20, 50],
                index=1,
                key="por_pagina"
            )
        
        # Determinar modo de búsqueda
        if busqueda_rapida:
            lista = buscar_usuarios(busqueda_rapida)
            total_usuarios = len(lista)
            total_paginas = 1
            pagina_actual = 1
            
            st.markdown(f"""
                <div class="pagination-info">
                    🔍 {total_usuarios} usuarios encontrados para "{busqueda_rapida}"
                </div>
            """, unsafe_allow_html=True)
            
        else:
            if "pagina_actual" not in st.session_state:
                st.session_state.pagina_actual = 1
            
            with col_config2:
                if st.button("⬅️ Anterior", key="btn_anterior", disabled=st.session_state.get("pagina_actual", 1) <= 1):
                    st.session_state.pagina_actual -= 1
                    st.rerun()
            
            with col_config3:
                resultado = get_usuarios_paginados(
                    filtro_nombre=filtro_nombre,
                    filtro_correo=filtro_correo,
                    filtro_rol=filtro_rol,
                    pagina=st.session_state.pagina_actual,
                    por_pagina=por_pagina
                )
                
                lista = resultado["usuarios"]
                total_usuarios = resultado["total"]
                total_paginas = resultado["total_paginas"]
                pagina_actual = resultado["pagina"]
                
                if st.button("➡️ Siguiente", key="btn_siguiente", disabled=pagina_actual >= total_paginas):
                    st.session_state.pagina_actual += 1
                    st.rerun()
            
            with col_config4:
                st.metric("Total", total_usuarios, delta=None)
            
            st.markdown(f"""
                <div class="pagination-info">
                    📄 Página {pagina_actual} de {total_paginas}
                </div>
            """, unsafe_allow_html=True)
            
            if pagina_actual > total_paginas and total_paginas > 0:
                st.session_state.pagina_actual = total_paginas
                st.rerun()

        if not lista:
            st.markdown("""
                <div class="info-box">
                    <h3 style="margin:0;">📭 No hay usuarios</h3>
                    <p style="margin:0.5rem 0 0 0;">No se encontraron usuarios que coincidan con los filtros aplicados.</p>
                </div>
            """, unsafe_allow_html=True)
            return

        #  MOSTRAR USUARIOS EN CARDS
        st.markdown("### 👥 Usuarios registrados")
        
        for usuario in lista:
            badge_class = "badge-admin" if usuario['rol'] == "admin" else "badge-empleado"
            badge_icon = "👑" if usuario['rol'] == "admin" else "👤"
            
            with st.expander(
                f"{badge_icon} {usuario['nombre']} • {usuario['correo']}", 
                expanded=False
            ):
                st.markdown(f"""
                    <div style="text-align: right;">
                        <span class="{badge_class}">{usuario['rol'].upper()}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("#### ✏️ Editar información")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_nombre = st.text_input(
                        "👤 Nombre completo",
                        value=usuario["nombre"],
                        key=f"nombre_{usuario['_id']}"
                    )
                    
                    new_correo = st.text_input(
                        "📧 Correo electrónico",
                        value=usuario["correo"],
                        key=f"correo_{usuario['_id']}"
                    )
                
                with col2:
                    new_rol = st.selectbox(
                        "🎭 Rol del usuario",
                        ["admin", "empleado"],
                        index=0 if usuario["rol"] == "admin" else 1,
                        key=f"rol_{usuario['_id']}"
                    )
                    
                    nueva_password = st.text_input(
                        "🔒 Nueva contraseña",
                        type="password",
                        placeholder="Dejar vacío para mantener actual",
                        help="Mínimo 6 caracteres",
                        key=f"password_{usuario['_id']}"
                    )
                
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                
                with col_btn1:
                    if st.button(
                        "💾 Guardar cambios", 
                        key=f"save_{usuario['_id']}",
                        type="primary",
                        use_container_width=True
                    ):
                        if not new_nombre or not new_correo:
                            st.session_state.mensaje = "Nombre y correo son obligatorios."
                            st.session_state.tipo_mensaje = "warning"
                            st.rerun()
                        
                        password_actualizada = nueva_password if nueva_password else None
                        if password_actualizada and len(password_actualizada) < 6:
                            st.session_state.mensaje = "La contraseña debe tener al menos 6 caracteres."
                            st.session_state.tipo_mensaje = "warning"
                            st.rerun()
                        
                        try:
                            update_usuario(
                                usuario["_id"],
                                new_nombre,
                                new_correo,
                                new_rol,
                                password_actualizada
                            )
                            msg = "Usuario y contraseña actualizados." if password_actualizada else "Usuario actualizado."
                            st.session_state.mensaje = msg
                            st.session_state.tipo_mensaje = "success"
                            st.rerun()
                        except Exception as e:
                            st.session_state.mensaje = f"Error: {str(e)}"
                            st.session_state.tipo_mensaje = "error"
                            st.rerun()

                with col_btn2:
                    if st.button(
                        "🗑️ Eliminar", 
                        key=f"delete_{usuario['_id']}",
                        use_container_width=True
                    ):
                        try:
                            delete_usuario(usuario["_id"])
                            st.session_state.mensaje = "Usuario eliminado correctamente."
                            st.session_state.tipo_mensaje = "success"
                            st.rerun()
                        except Exception as e:
                            st.session_state.mensaje = f"Error: {str(e)}"
                            st.session_state.tipo_mensaje = "error"
                            st.rerun()
                
                with col_btn3:
                    if st.button(
                        "🔄 Restablecer", 
                        key=f"reset_{usuario['_id']}",
                        use_container_width=True
                    ):
                        st.rerun()

        # 🔹 NAVEGACIÓN INFERIOR
        if not busqueda_rapida and total_paginas > 1:
            st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
            col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
            
            with col_nav1:
                if st.button(
                    "⬅️ Anterior", 
                    key="btn_anterior_inf", 
                    use_container_width=True,
                    disabled=pagina_actual <= 1
                ):
                    st.session_state.pagina_actual -= 1
                    st.rerun()
            
            with col_nav2:
                st.markdown(f"""
                    <div style="text-align: center; padding: 0.5rem;">
                        <strong>Página {pagina_actual} de {total_paginas}</strong>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_nav3:
                if st.button(
                    "➡️ Siguiente", 
                    key="btn_siguiente_inf", 
                    use_container_width=True,
                    disabled=pagina_actual >= total_paginas
                ):
                    st.session_state.pagina_actual += 1
                    st.rerun()