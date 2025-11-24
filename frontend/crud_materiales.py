import streamlit as st
from backend.controllers.materiales_controller import (
    create_material_controller,
    get_materiales_paginados,
    buscar_materiales,
    update_material,
    delete_material,
    get_material_by_id,
    get_lugares_para_materiales,
)


# ESTILOS CSS PERSONALIZADOS
def aplicar_estilos():
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
        
        /* Cards de material */
        .material-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .material-card:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        /* Badges de estado */
        .badge-stock {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .badge-sin-stock {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
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
        
        /* Indicadores de stock */
        .stock-bajo {
            color: #f5576c;
            font-weight: 700;
        }
        
        .stock-normal {
            color: #4facfe;
            font-weight: 700;
        }
        
        .stock-alto {
            color: #5eead4;
            font-weight: 700;
        }
        </style>
    """, unsafe_allow_html=True)


# COMPONENTE DE AYUDA
def help_info():
    with st.expander("ℹ Ayuda del módulo de Materiales"):
        st.markdown("""
        **📦 En este módulo puedes:**
        - Registrar nuevos materiales
        - Editar materiales existentes  
        - Eliminar materiales
        - Buscar rápidamente por clave, descripción o genérico
        - Aplicar filtros y paginación

        **🎯 Importante:**
        - La **clave del material debe ser única**
        - La **existencia y costo** deben ser números válidos
        - La **eliminación es permanente**
        - Puedes asignar materiales a **lugares específicos**
        """)


# FORMULARIO BASE (Crear / Editar)

def formulario_material(material=None, key_suffix=""):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        clave = st.text_input(
            "🔑 Clave del material *",
            value=material["clave_material"] if material else "",
            placeholder="MAT-001",
            help="Clave única identificadora del material",
            key=f"clave_{key_suffix}"
        )
        
        descripcion = st.text_input(
            "📝 Descripción *",
            value=material["descripcion"] if material else "",
            placeholder="Descripción detallada del material",
            help="Describe claramente el material",
            key=f"descripcion_{key_suffix}"
        )
        
        generico = st.text_input(
            "🏷️ Genérico",
            value=material["generico"] if material else "",
            placeholder="Tipo genérico o categoría",
            help="Clasificación general del material",
            key=f"generico_{key_suffix}"
        )
    
    with col2:
        clasificacion = st.text_input(
            "📊 Clasificación",
            value=material["clasificacion"] if material else "",
            placeholder="Categoría específica",
            help="Clasificación técnica o funcional",
            key=f"clasificacion_{key_suffix}"
        )
        
        existencia = st.number_input(
            "📦 Existencia *",
            value=float(material["existencia"]) if material else 0.0, 
            min_value=0.0,
            step=1.0,
            help="Cantidad disponible en inventario",
            key=f"existencia_{key_suffix}"
        )
        
        costo = st.number_input(
            "💰 Costo promedio *",
            value=float(material["costo_promedio"]) if material else 0.0, 
            min_value=0.0,
            step=0.01,
            format="%.2f",
            help="Costo unitario promedio",
            key=f"costo_{key_suffix}"
        )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Dropdown de lugares
    st.markdown("### 📍 Asignación de Lugar")
    lugares = get_lugares_para_materiales()
    
    # Crear opciones para el selectbox
    opciones_lugares = ["Seleccionar lugar"] + [f"{lugar['_id']}" for lugar in lugares]
    nombres_lugares = ["Seleccionar lugar"] + [f"{lugar['nombre']} - {lugar['estado']}" for lugar in lugares]
    
    # Encontrar el índice seleccionado si estamos editando
    indice_seleccionado = 0  # Por defecto "Seleccionar lugar"
    if material and material.get("lugar_id"):
        try:
            lugar_actual = material["lugar_id"]
            for i, lugar in enumerate(lugares, 1):  # Empezar desde 1 porque 0 es "Seleccionar lugar"
                if str(lugar["_id"]) == lugar_actual:
                    indice_seleccionado = i
                    break
        except:
            indice_seleccionado = 0
    
    # Mostrar el dropdown CON KEY ÚNICA
    seleccion = st.selectbox(
        "🏢 Lugar de almacenamiento",
        options=range(len(nombres_lugares)),
        index=indice_seleccionado,
        format_func=lambda x: nombres_lugares[x],
        help="Selecciona el lugar donde se almacena el material",
        key=f"lugar_select_{key_suffix}"  # ¡KEY ÚNICA AQUÍ!
    )
    
    # Obtener el lugar_id seleccionado
    lugar_id = None
    if seleccion > 0:  # Si no es "Seleccionar lugar"
        lugar_id = opciones_lugares[seleccion]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return clave, descripcion, generico, clasificacion, existencia, costo, lugar_id



# CRUD PRINCIPAL

def crud_materiales():
    
    # Aplicar estilos personalizados
    aplicar_estilos()
    
    # 🎯 HEADER PRINCIPAL
    st.markdown("""
        <div class="header-principal">
            <h1>📦 Gestión de Materiales</h1>
            <p>Administra el inventario de materiales de manera eficiente</p>
        </div>
    """, unsafe_allow_html=True)
    
    #  INICIALIZAR ESTADO PARA MENSAJES
    if "mensaje" not in st.session_state:
        st.session_state.mensaje = None
    if "tipo_mensaje" not in st.session_state:
        st.session_state.tipo_mensaje = None
    
    # MOSTRAR MENSAJES EXISTENTES
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

    # Componente de ayuda
    help_info()

    # SELECTOR DE ACCIÓN CON TABS
    tab1, tab2 = st.tabs(["➕ Crear Material", "📋 Gestionar Materiales"])

    #   CREAR MATERIAL
    with tab1:
        st.markdown("### ✨ Registrar nuevo material")
        st.markdown("Completa el formulario para agregar un nuevo material al inventario.")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # USAR KEY ÚNICA PARA CREACIÓN
        clave, descripcion, generico, clasificacion, existencia, costo, lugar_id = formulario_material(key_suffix="create")

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("✨ Crear material", type="primary", use_container_width=True, key="btn_crear_material"):
                if not clave or not descripcion:
                    st.session_state.mensaje = "La clave y descripción son obligatorias."
                    st.session_state.tipo_mensaje = "warning"
                    st.rerun()

                if existencia < 0 or costo < 0:
                    st.session_state.mensaje = "La existencia y costo deben ser valores positivos."
                    st.session_state.tipo_mensaje = "warning"
                    st.rerun()

                resultado = create_material_controller(
                    clave, descripcion, generico, clasificacion,
                    existencia, costo, lugar_id
                )

                if "error" in resultado:
                    st.session_state.mensaje = resultado["error"]
                    st.session_state.tipo_mensaje = "error"
                    st.rerun()
                else:
                    st.session_state.mensaje = "Material creado exitosamente."
                    st.session_state.tipo_mensaje = "success"
                    st.rerun()

    
    # LISTAR / EDITAR / ELIMINAR
    with tab2:
        # 🔍 SECCIÓN DE BÚSQUEDA Y FILTROS
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 Búsqueda y Filtros")
        
        # Búsqueda rápida destacada
        busqueda_rapida = st.text_input(
            "⚡ Búsqueda rápida",
            placeholder="🔎 Busca por clave, descripción o genérico...",
            key="busqueda_rapida_materiales",
            label_visibility="collapsed"
        )
        
        with st.expander("🎛️ Filtros avanzados", expanded=False):
            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                filtro_clave = st.text_input(
                    "🔑 Clave",
                    placeholder="Filtrar por clave",
                    key="filtro_clave_materiales"
                )
            
            with col_filtro2:
                filtro_descripcion = st.text_input(
                    "📝 Descripción",
                    placeholder="Filtrar por descripción",
                    key="filtro_descripcion_materiales"
                )
            
            with col_filtro3:
                filtro_generico = st.text_input(
                    "🏷️ Genérico",
                    placeholder="Filtrar por genérico",
                    key="filtro_generico_materiales"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # CONFIGURACIÓN DE PAGINACIÓN
        col_config1, col_config2, col_config3, col_config4 = st.columns([1, 1, 1, 1])
        
        with col_config1:
            por_pagina = st.selectbox(
                "📄 Por página",
                [5, 10, 20, 50],
                index=1,
                key="por_pagina_materiales"
            )
        
        # Determinar modo de búsqueda
        if busqueda_rapida:
            lista = buscar_materiales(busqueda_rapida)
            total_materiales = len(lista)
            total_paginas = 1
            pagina_actual = 1
            
            st.markdown(f"""
                <div class="pagination-info">
                    🔍 {total_materiales} materiales encontrados para "{busqueda_rapida}"
                </div>
            """, unsafe_allow_html=True)
            
        else:
            if "pagina_actual_materiales" not in st.session_state:
                st.session_state.pagina_actual_materiales = 1
            
            with col_config2:
                if st.button("⬅️ Anterior", key="btn_anterior_materiales", disabled=st.session_state.get("pagina_actual_materiales", 1) <= 1):
                    st.session_state.pagina_actual_materiales -= 1
                    st.rerun()
            
            with col_config3:
                resultado = get_materiales_paginados(
                    filtro_clave=filtro_clave,
                    filtro_descripcion=filtro_descripcion,
                    filtro_generico=filtro_generico,
                    pagina=st.session_state.pagina_actual_materiales,
                    por_pagina=por_pagina
                )
                
                lista = resultado["materiales"]
                total_materiales = resultado["total"]
                total_paginas = resultado["total_paginas"]
                pagina_actual = resultado["pagina"]
                
                if st.button("➡️ Siguiente", key="btn_siguiente_materiales", disabled=pagina_actual >= total_paginas):
                    st.session_state.pagina_actual_materiales += 1
                    st.rerun()
            
            with col_config4:
                st.metric("Total", total_materiales, delta=None)
            
            st.markdown(f"""
                <div class="pagination-info">
                    📄 Página {pagina_actual} de {total_paginas}
                </div>
            """, unsafe_allow_html=True)
            
            if pagina_actual > total_paginas and total_paginas > 0:
                st.session_state.pagina_actual_materiales = total_paginas
                st.rerun()

        if not lista:
            st.markdown("""
                <div class="info-box">
                    <h3 style="margin:0;">📭 No hay materiales</h3>
                    <p style="margin:0.5rem 0 0 0;">No se encontraron materiales que coincidan con los filtros aplicados.</p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            #  MOSTRAR MATERIALES EN CARDS
            st.markdown("### 📦 Materiales en inventario")
            
            for i, material in enumerate(lista):
                # Determinar clase de stock
                stock_clase = "stock-bajo" if material['existencia'] == 0 else "stock-normal" if material['existencia'] < 10 else "stock-alto"
                badge_class = "badge-sin-stock" if material['existencia'] == 0 else "badge-stock"
                badge_text = "SIN STOCK" if material['existencia'] == 0 else f"STOCK: {material['existencia']}"

                with st.expander(
    f"🔑 {material['clave_material']} • {material['descripcion'][:50]}...", 
    expanded=False
):

                    st.markdown(f"""
                        <div style="text-align: right;">
                            <span class="{badge_class}">{badge_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.markdown("#### 📋 Información General")
                        st.write(f"**🔑 Clave:** {material['clave_material']}")
                        st.write(f"**📝 Descripción:** {material['descripcion']}")
                        st.write(f"**🏷️ Genérico:** {material.get('generico', 'No especificado')}")
                        st.write(f"**📊 Clasificación:** {material.get('clasificacion', 'No especificada')}")
                    
                    with col_info2:
                        st.markdown("#### 💰 Detalles de Inventario")
                        st.write(f"**📦 Existencia:** <span class='{stock_clase}'>{material['existencia']} unidades</span>", unsafe_allow_html=True)
                        st.write(f"**💰 Costo promedio:** ${material['costo_promedio']:,.2f}")
                        
                        # Mostrar información del lugar
                        if material.get('lugar_nombre'):
                            st.write(f"**📍 Lugar:** {material['lugar_nombre']} - {material['lugar_estado']}")
                        elif material.get('lugar_id'):
                            st.write(f"**📍 Lugar ID:** {material['lugar_id']}")
                        else:
                            st.write("**📍 Lugar:** No asignado")
                    
                    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                    
                    st.markdown("#### ✏️ Editar información")
                    
                    new_clave, new_descripcion, new_generico, new_clasificacion, new_existencia, new_costo, new_lugar_id = formulario_material(
                        material=material, 
                        key_suffix=f"edit_{material['_id']}"
                    )
                    
                    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                    
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    with col_btn1:
                        if st.button(
                            "💾 Guardar cambios", 
                            key=f"save_{material['_id']}",
                            type="primary",
                            use_container_width=True
                        ):
                            if not new_clave or not new_descripcion:
                                st.session_state.mensaje = "Clave y descripción son obligatorios."
                                st.session_state.tipo_mensaje = "warning"
                                st.rerun()
                            
                            if new_existencia < 0 or new_costo < 0:
                                st.session_state.mensaje = "Existencia y costo deben ser valores positivos."
                                st.session_state.tipo_mensaje = "warning"
                                st.rerun()
                            
                            try:
                                resultado = update_material(
                                    material["_id"],
                                    new_clave,
                                    new_descripcion,
                                    new_generico,
                                    new_clasificacion,
                                    new_existencia,
                                    new_costo,
                                    new_lugar_id
                                )
                                
                                if "error" in resultado:
                                    st.session_state.mensaje = resultado["error"]
                                    st.session_state.tipo_mensaje = "error"
                                else:
                                    st.session_state.mensaje = "Material actualizado exitosamente."
                                    st.session_state.tipo_mensaje = "success"
                                st.rerun()
                            except Exception as e:
                                st.session_state.mensaje = f"Error: {str(e)}"
                                st.session_state.tipo_mensaje = "error"
                                st.rerun()

                    with col_btn2:
                        if st.button(
                            "🗑️ Eliminar", 
                            key=f"delete_{material['_id']}",
                            use_container_width=True
                        ):
                            try:
                                delete_material(material["_id"])
                                st.session_state.mensaje = "Material eliminado correctamente."
                                st.session_state.tipo_mensaje = "success"
                                st.rerun()
                            except Exception as e:
                                st.session_state.mensaje = f"Error: {str(e)}"
                                st.session_state.tipo_mensaje = "error"
                                st.rerun()
                    
                    with col_btn3:
                        if st.button(
                            "🔄 Restablecer", 
                            key=f"reset_{material['_id']}",
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
                        key="btn_anterior_inf_materiales", 
                        use_container_width=True,
                        disabled=pagina_actual <= 1
                    ):
                        st.session_state.pagina_actual_materiales -= 1
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
                        key="btn_siguiente_inf_materiales", 
                        use_container_width=True,
                        disabled=pagina_actual >= total_paginas
                    ):
                        st.session_state.pagina_actual_materiales += 1
                        st.rerun()

    # EDITAR MATERIAL (MODO ANTIGUO - como respaldo)
    
    if "editar_material_id" in st.session_state:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### ✏️ Edición Rápida de Material")
        
        material_id = st.session_state["editar_material_id"]
        material = get_material_by_id(material_id)

        if not material:
            st.error("❌ Material no encontrado.")
            del st.session_state["editar_material_id"]
            st.rerun()

        clave, descripcion, generico, clasificacion, existencia, costo, lugar_id = formulario_material(
            material=material, 
            key_suffix=f"quick_edit_{material_id}"
        )

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Actualizar material", type="primary", use_container_width=True, key=f"quick_save_{material_id}"):
                resultado = update_material(
                    material_id,
                    clave,
                    descripcion,
                    generico,
                    clasificacion,
                    existencia,
                    costo,
                    lugar_id
                )
                if "error" in resultado:
                    st.session_state.mensaje = resultado["error"]
                    st.session_state.tipo_mensaje = "error"
                else:
                    st.session_state.mensaje = "Material actualizado exitosamente."
                    st.session_state.tipo_mensaje = "success"
                    del st.session_state["editar_material_id"]
                st.rerun()
        
        with col2:
            if st.button("❌ Cancelar edición", use_container_width=True, key=f"quick_cancel_{material_id}"):
                del st.session_state["editar_material_id"]
                st.rerun()