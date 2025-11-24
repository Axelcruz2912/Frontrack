import streamlit as st
from backend.controllers.lugares_controller import (
    create_lugar_controller,
    get_lugares_paginados,
    buscar_lugares,
    update_lugar,
    delete_lugar,
    get_lugar_by_id,
)


def crud_lugares():
    #  ESTILOS CSS PERSONALIZADOS
    st.markdown("""
        <style>
        /* Estilos globales */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header principal */
        .header-lugares {
            background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(48, 207, 208, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-lugares h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-lugares p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }
        
        /* Cards de lugar */
        .lugar-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            border-left: 4px solid #30cfd0;
            transition: all 0.3s ease;
        }
        
        .lugar-card:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        /* Info boxes */
        .info-lugar {
            background: linear-gradient(135deg, #30cfd015 0%, #33086715 100%);
            border-left: 4px solid #30cfd0;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Stats */
        .stat-lugar {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .stat-lugar-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #30cfd0;
        }
        
        .stat-lugar-label {
            color: #666;
            font-size: 0.85rem;
            margin-top: 0.3rem;
        }
        
        /* Badges de estado */
        .badge-estado {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
        }
        
        /* Search section */
        .search-lugares {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
        }
        
        /* Form container */
        .form-lugares {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        }
        
        /* Divider */
        .divider-lugares {
            height: 2px;
            background: linear-gradient(90deg, transparent, #30cfd0, transparent);
            margin: 1.5rem 0;
        }
        
        /* Lugar info grid */
        .lugar-info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }
        
        .lugar-info-item {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            border-left: 3px solid #30cfd0;
        }
        
        .lugar-info-label {
            font-size: 0.75rem;
            color: #666;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
            font-weight: 600;
        }
        
        .lugar-info-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
        }
        
        /* Pagination */
        .pagination-lugares {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            font-weight: 600;
            margin: 1rem 0;
        }
        
        /* Help box */
        .help-lugares {
            background: linear-gradient(135deg, #d299c2 0%, #fef9d7 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }
        
        .help-lugares h2 {
            margin-top: 0;
            color: #333;
        }
        
        /* Location pin icon */
        .location-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 1.2rem;
            font-weight: 600;
            color: #30cfd0;
            margin-bottom: 1rem;
        }
        
        /* Map container */
        .map-container {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 2px dashed #30cfd0;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* Empty state */
        .empty-state {
            text-align: center;
            padding: 3rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        .empty-state-icon {
            font-size: 4rem;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    #  HEADER PRINCIPAL
    st.markdown("""
        <div class="header-lugares">
            <h1>🏢 Gestión de Lugares</h1>
            <p>Administra ubicaciones y sucursales de tu organización</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 🔹 INICIALIZAR ESTADO
    if "mensaje_lugar" not in st.session_state:
        st.session_state.mensaje_lugar = None
    if "tipo_mensaje_lugar" not in st.session_state:
        st.session_state.tipo_mensaje_lugar = None
    if "pagina_lugar" not in st.session_state:
        st.session_state.pagina_lugar = 1
    
    # 🔹 MOSTRAR MENSAJES
    if st.session_state.mensaje_lugar:
        if st.session_state.tipo_mensaje_lugar == "success":
            st.success(f"✅ {st.session_state.mensaje_lugar}")
        elif st.session_state.tipo_mensaje_lugar == "error":
            st.error(f"❌ {st.session_state.mensaje_lugar}")
        elif st.session_state.tipo_mensaje_lugar == "warning":
            st.warning(f"⚠️ {st.session_state.mensaje_lugar}")
        elif st.session_state.tipo_mensaje_lugar == "info":
            st.info(f"ℹ️ {st.session_state.mensaje_lugar}")
        
        st.session_state.mensaje_lugar = None
        st.session_state.tipo_mensaje_lugar = None
    
    #  TABS PRINCIPALES
    tab1, tab2, tab3 = st.tabs(["🗺️ Directorio de Lugares", "➕ Nuevo Lugar", "ℹ️ Ayuda"])
    
    # TAB 1: DIRECTORIO Y GESTIÓN
    with tab1:
        # 🔍 BÚSQUEDA RÁPIDA
        st.markdown('<div class="search-lugares">', unsafe_allow_html=True)
        st.markdown("### 🔍 Búsqueda Rápida")
        
        termino = st.text_input(
            "Buscar lugar",
            placeholder="🔎 Busca por nombre o estado...",
            key="busqueda_rapida_lugar",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Resultados de búsqueda rápida
        if termino:
            resultados = buscar_lugares(termino)
            
            st.markdown(f"""
                <div class="pagination-lugares">
                    🔍 {len(resultados)} lugares encontrados para "{termino}"
                </div>
            """, unsafe_allow_html=True)
            
            if resultados:
                # Mostrar como grid de cards
                for l in resultados:
                    with st.expander(f"📍 {l['nombre']} — {l['estado']}", expanded=False):
                        st.markdown(f"""
                            <div class="location-header">
                                <span>📍</span>
                                <span>{l['nombre']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                                <div class="lugar-info-item">
                                    <div class="lugar-info-label">🏛️ Nombre del Lugar</div>
                                    <div class="lugar-info-value">{l['nombre']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                                <div class="lugar-info-item">
                                    <div class="lugar-info-label">🗾 Estado/Región</div>
                                    <div class="lugar-info-value">{l['estado']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown(f"""
                            <div class="map-container">
                                <span style="font-size: 2rem;">🗺️</span>
                                <p style="margin: 0.5rem 0 0 0; color: #666;">
                                    <strong>ID:</strong> {l['_id']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
                        
                        col_btn1, col_btn2, col_btn3 = st.columns(3)
                        
                        with col_btn1:
                            if st.button("✏️ Editar", key=f"edit_search_{l['_id']}", use_container_width=True):
                                st.session_state["editar_lugar_id"] = str(l["_id"])
                                st.rerun()
                        
                        with col_btn2:
                            if st.button("🗑️ Eliminar", key=f"del_search_{l['_id']}", use_container_width=True):
                                delete_lugar(str(l["_id"]))
                                st.session_state.mensaje_lugar = "Lugar eliminado correctamente."
                                st.session_state.tipo_mensaje_lugar = "success"
                                st.rerun()
                        
                        with col_btn3:
                            if st.button("📋 Ver ID", key=f"id_search_{l['_id']}", use_container_width=True):
                                st.info(f"**ID:** {l['_id']}")
            else:
                st.markdown("""
                    <div class="empty-state">
                        <div class="empty-state-icon">🔍</div>
                        <h3>No se encontraron resultados</h3>
                        <p>Intenta con otros términos de búsqueda</p>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
        
        # FILTROS AVANZADOS Y LISTADO PAGINADO
        st.markdown("### 🎛️ Filtros Avanzados")
        
        with st.expander("🔧 Configurar filtros", expanded=not termino):
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                filtro_nombre = st.text_input(
                    "🏛️ Nombre",
                    placeholder="Filtrar por nombre",
                    key="filtro_nombre"
                )
            
            with col_f2:
                filtro_estado = st.text_input(
                    "🗾 Estado",
                    placeholder="Filtrar por estado",
                    key="filtro_estado"
                )
        
        # Paginación
        col_pag1, col_pag2, col_pag3, col_pag4 = st.columns([1, 1, 1, 1])
        
        with col_pag1:
            por_pagina = st.selectbox(
                "📄 Por página",
                [5, 10, 20, 50],
                index=1,
                key="por_pagina_lugar"
            )
        
        datos = get_lugares_paginados(
            filtro_nombre=filtro_nombre,
            filtro_estado=filtro_estado,
            pagina=st.session_state.pagina_lugar,
            por_pagina=por_pagina
        )
        
        lista = datos["lugares"]
        total_lugares = datos["total"]
        total_paginas = datos["total_paginas"]
        pagina_actual = datos["pagina"]
        
        with col_pag2:
            if st.button("⬅️ Anterior", key="btn_ant_lug", disabled=pagina_actual <= 1):
                st.session_state.pagina_lugar -= 1
                st.rerun()
        
        with col_pag3:
            if st.button("➡️ Siguiente", key="btn_sig_lug", disabled=pagina_actual >= total_paginas):
                st.session_state.pagina_lugar += 1
                st.rerun()
        
        with col_pag4:
            st.metric("Total", total_lugares)
        
        st.markdown(f"""
            <div class="pagination-lugares">
                📄 Página {pagina_actual} de {total_paginas}
            </div>
        """, unsafe_allow_html=True)
        
        #  LISTADO DE LUGARES
        if not lista and not termino:
            st.markdown("""
                <div class="empty-state">
                    <div class="empty-state-icon">🏢</div>
                    <h3>No hay lugares registrados</h3>
                    <p>Comienza agregando un nuevo lugar en la pestaña "Nuevo Lugar"</p>
                </div>
            """, unsafe_allow_html=True)
        elif not termino:
            st.markdown("### 🗺️ Directorio de Lugares")
            
            for l in lista:
                with st.expander(f"📍 {l['nombre']} — {l['estado']}", expanded=False):
                    st.markdown(f"""
                        <div class="location-header">
                            <span>📍</span>
                            <span>{l['nombre']}</span>
                        </div>
                        <span class="badge-estado">{l['estado']}</span>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                            <div class="lugar-info-item">
                                <div class="lugar-info-label">🏛️ Nombre Completo</div>
                                <div class="lugar-info-value">{l['nombre']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                            <div class="lugar-info-item">
                                <div class="lugar-info-label">🗾 Estado/Región</div>
                                <div class="lugar-info-value">{l['estado']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="map-container">
                            <span style="font-size: 2rem;">🗺️</span>
                            <p style="margin: 0.5rem 0 0 0; color: #666;">
                                <strong>Identificador:</strong> {l['_id']}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
                    
                    col_a1, col_a2, col_a3 = st.columns(3)
                    
                    with col_a1:
                        if st.button("✏️ Editar", key=f"edit_{l['_id']}", type="primary", use_container_width=True):
                            st.session_state["editar_lugar_id"] = str(l["_id"])
                            st.rerun()
                    
                    with col_a2:
                        if st.button("🗑️ Eliminar", key=f"del_{l['_id']}", use_container_width=True):
                            delete_lugar(str(l["_id"]))
                            st.session_state.mensaje_lugar = "Lugar eliminado correctamente."
                            st.session_state.tipo_mensaje_lugar = "success"
                            st.rerun()
                    
                    with col_a3:
                        if st.button("📋 Copiar ID", key=f"copy_{l['_id']}", use_container_width=True):
                            st.code(l['_id'], language=None)
            
            # Navegación inferior
            if total_paginas > 1:
                st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
                col_nav1, col_nav2, col_nav3 = st.columns([1, 2, 1])
                
                with col_nav1:
                    if st.button("⬅️ Anterior", key="nav_ant_inf", use_container_width=True, disabled=pagina_actual <= 1):
                        st.session_state.pagina_lugar -= 1
                        st.rerun()
                
                with col_nav2:
                    st.markdown(f"""
                        <div style="text-align: center; padding: 0.5rem;">
                            <strong>Página {pagina_actual} de {total_paginas}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_nav3:
                    if st.button("➡️ Siguiente", key="nav_sig_inf", use_container_width=True, disabled=pagina_actual >= total_paginas):
                        st.session_state.pagina_lugar += 1
                        st.rerun()
        
        
        # EDITAR LUGAR (Modal)
        if "editar_lugar_id" in st.session_state:
            st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
            st.markdown("### ✏️ Editar Lugar")
            
            lugar_id = st.session_state["editar_lugar_id"]
            lugar = get_lugar_by_id(lugar_id)
            
            if not lugar:
                st.error("Lugar no encontrado.")
                del st.session_state["editar_lugar_id"]
            else:
                st.markdown('<div class="form-lugares">', unsafe_allow_html=True)
                
                col_e1, col_e2 = st.columns(2)
                
                with col_e1:
                    nombre = st.text_input(
                        "🏛️ Nombre del lugar", 
                        value=lugar["nombre"], 
                        key="edit_nombre",
                        placeholder="Nombre completo del lugar"
                    )
                
                with col_e2:
                    estado = st.text_input(
                        "🗾 Estado/Región", 
                        value=lugar["estado"], 
                        key="edit_estado",
                        placeholder="Estado o región"
                    )
                
                st.markdown(f"""
                    <div class="info-lugar">
                        <strong>📍 ID del lugar:</strong> {lugar_id}
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
                
                col_btn_e1, col_btn_e2, col_btn_e3 = st.columns(3)
                
                with col_btn_e1:
                    if st.button("💾 Guardar cambios", type="primary", use_container_width=True, key="save_edit"):
                        if not nombre:
                            st.session_state.mensaje_lugar = "El nombre del lugar es obligatorio."
                            st.session_state.tipo_mensaje_lugar = "warning"
                            st.rerun()
                        
                        try:
                            update_lugar(lugar_id, nombre, estado)
                            st.session_state.mensaje_lugar = "Lugar actualizado correctamente."
                            st.session_state.tipo_mensaje_lugar = "success"
                            del st.session_state["editar_lugar_id"]
                            st.rerun()
                        except Exception as e:
                            st.session_state.mensaje_lugar = f"Error: {str(e)}"
                            st.session_state.tipo_mensaje_lugar = "error"
                            st.rerun()
                
                with col_btn_e2:
                    if st.button("❌ Cancelar", use_container_width=True, key="cancel_edit"):
                        del st.session_state["editar_lugar_id"]
                        st.rerun()
                
                with col_btn_e3:
                    if st.button("🔄 Restablecer", use_container_width=True, key="reset_edit"):
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    
    # TAB 2: CREAR LUGAR
    with tab2:
        st.markdown('<div class="form-lugares">', unsafe_allow_html=True)
        st.markdown("### ✨ Registrar Nuevo Lugar")
        st.markdown("Agrega una nueva ubicación o sucursal a tu sistema.")
        st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            nombre_new = st.text_input(
                "🏛️ Nombre del lugar",
                placeholder="Ej: Oficina Central, Sucursal Norte, etc.",
                key="new_nombre",
                help="El nombre debe ser único en el sistema"
            )
        
        with col_c2:
            estado_new = st.text_input(
                "🗾 Estado/Región",
                placeholder="Ej: Ciudad de México, Jalisco, etc.",
                key="new_estado",
                help="Estado o región donde se ubica"
            )
        
        st.markdown("""
            <div class="info-lugar">
                <strong>💡 Consejo:</strong> Usa nombres descriptivos que te ayuden a identificar 
                rápidamente cada ubicación.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
        
        col_btn_c1, col_btn_c2, col_btn_c3 = st.columns([1, 2, 1])
        
        with col_btn_c2:
            if st.button("✨ Crear Lugar", type="primary", use_container_width=True, key="create_lugar"):
                if not nombre_new:
                    st.session_state.mensaje_lugar = "El nombre del lugar es obligatorio."
                    st.session_state.tipo_mensaje_lugar = "error"
                    st.rerun()
                
                resp = create_lugar_controller(nombre_new, estado_new)
                
                if "error" in resp:
                    st.session_state.mensaje_lugar = resp["error"]
                    st.session_state.tipo_mensaje_lugar = "error"
                    st.rerun()
                else:
                    st.session_state.mensaje_lugar = "Lugar registrado correctamente."
                    st.session_state.tipo_mensaje_lugar = "success"
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Vista previa
        if nombre_new or estado_new:
            st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
            st.markdown("### 👁️ Vista Previa")
            st.markdown('<div class="lugar-card">', unsafe_allow_html=True)
            st.markdown(f"""
                <div class="location-header">
                    <span>📍</span>
                    <span>{nombre_new if nombre_new else 'Nombre del lugar'}</span>
                </div>
                <span class="badge-estado">{estado_new if estado_new else 'Estado/Región'}</span>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    
    # TAB 3: AYUDA
    with tab3:
        st.markdown("""
            <div class="help-lugares">
                <h2>ℹ️ Ayuda del Módulo de Lugares</h2>
                <p>Aprende a gestionar las ubicaciones de tu organización.</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_help1, col_help2 = st.columns(2)
        
        with col_help1:
            st.markdown("""
                <div class="info-lugar">
                    <h3>🎯 Funcionalidades</h3>
                    <ul>
                        <li><strong>Registrar lugares:</strong> Agrega nuevas ubicaciones</li>
                        <li><strong>Editar información:</strong> Actualiza datos existentes</li>
                        <li><strong>Eliminar lugares:</strong> Remueve ubicaciones obsoletas</li>
                        <li><strong>Búsqueda rápida:</strong> Encuentra lugares al instante</li>
                        <li><strong>Filtros avanzados:</strong> Refina tus búsquedas</li>
                        <li><strong>Paginación:</strong> Navega por grandes listas</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        with col_help2:
            st.markdown("""
                <div class="info-lugar">
                    <h3>⚠️ Importante</h3>
                    <ul>
                        <li>El <strong>nombre</strong> debe ser único</li>
                        <li>Campo obligatorio: Nombre del lugar</li>
                        <li>El estado/región es opcional pero recomendado</li>
                        <li>La eliminación es <strong>permanente</strong></li>
                        <li>Los cambios se guardan inmediatamente</li>
                        <li>Usa nombres descriptivos y claros</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-lugar">
                <h3>💡 Mejores Prácticas</h3>
                <p><strong>📍 Nomenclatura clara:</strong> Usa nombres que identifiquen rápidamente el lugar</p>
                <p><strong>🗾 Especifica el estado:</strong> Ayuda a organizar ubicaciones geográficamente</p>
                <p><strong>🔍 Usa la búsqueda rápida:</strong> Para encontrar lugares específicos al instante</p>
                <p><strong>🎛️ Aplica filtros:</strong> Para trabajar con subconjuntos de lugares</p>
                <p><strong>✏️ Mantén actualizado:</strong> Revisa y actualiza la información periódicamente</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-lugares"></div>', unsafe_allow_html=True)
        
        st.markdown("""
            <div class="map-container">
                <span style="font-size: 3rem;">🗺️</span>
                <h3 style="margin: 1rem 0 0.5rem 0;">Sistema de Gestión de Lugares</h3>
                <p style="margin: 0; color: #666;">
                    Organiza y administra todas las ubicaciones de tu empresa desde un solo lugar
                </p>
            </div>
        """, unsafe_allow_html=True)