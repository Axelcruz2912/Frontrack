import streamlit as st
from datetime import datetime
from backend.controllers.fallas_controller import (
    create_falla_controller,
    get_fallas_paginadas,
    buscar_fallas,
    update_falla,
    delete_falla,
    get_falla_by_id,
    get_lugares_para_fallas,
    get_usuarios_para_fallas,
    get_materiales_para_fallas
)


# 🎨 ESTILOS CSS PERSONALIZADOS
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
        
        /* Cards de falla */
        .falla-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .falla-card:hover {
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.12);
            transform: translateY(-2px);
        }
        
        /* Badges de estado */
        .badge-pendiente {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }
        
        .badge-completado {
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
        
        /* Material items */
        .material-item {
            background: #f8f9fa;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            margin: 0.25rem 0;
            border-left: 3px solid #667eea;
        }
        </style>
    """, unsafe_allow_html=True)


# ================================
# COMPONENTE DE AYUDA
# ================================
def help_info():
    with st.expander("ℹ Ayuda del módulo de Fallas"):
        st.markdown("""
        **🔧 En este módulo puedes:**
        - Registrar nuevas fallas/reportes
        - Asignar usuarios que reportan y revisan
        - Seleccionar lugares y materiales utilizados
        - Gestionar información de vehículos y conductores
        
        **🎯 Campos importantes:**
        - **Lugar:** Donde ocurrió la falla
        - **Usuario que reporta:** Quién identificó el problema
        - **Usuario que revisa:** Responsable de la revisión
        - **Materiales usados:** Insumos utilizados en la reparación
        - **Información del vehículo:** Datos del equipo involucrado
        """)


# ================================
# FORMULARIO BASE (Crear / Editar)
# ================================
def formulario_falla(falla=None, key_suffix=""):
    # Obtener datos para dropdowns
    lugares_lista = get_lugares_para_fallas()
    usuarios_lista = get_usuarios_para_fallas()
    materiales_lista = get_materiales_para_fallas()
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    # Información básica
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📍 Información de Ubicación")
        # Lugar
        opciones_lugares = [f"{lugar['_id']}" for lugar in lugares_lista]
        nombres_lugares = [f"{lugar['nombre']} - {lugar['estado']}" for lugar in lugares_lista]
        
        indice_lugar = 0
        if falla and falla.get("lugar_id"):
            try:
                for i, lugar in enumerate(lugares_lista):
                    if str(lugar["_id"]) == str(falla["lugar_id"]):
                        indice_lugar = i
                        break
            except:
                indice_lugar = 0
        
        seleccion_lugar = st.selectbox(
            "🏢 Lugar *",
            options=range(len(nombres_lugares)),
            index=indice_lugar,
            format_func=lambda x: nombres_lugares[x],
            key=f"lugar_{key_suffix}"
        )
        lugar_id = opciones_lugares[seleccion_lugar] if lugares_lista else None
        
        # Fecha
        fecha = st.date_input(
            "📅 Fecha de la falla *",
            value=falla["fecha"].date() if falla and falla.get("fecha") else datetime.now().date(),
            key=f"fecha_{key_suffix}"
        )
        
        # Nombre conductor
        nombre_conductor = st.text_input(
            "👤 Nombre del conductor *",
            value=falla["nombre_conductor"] if falla else "",
            placeholder="Nombre completo del conductor",
            key=f"conductor_{key_suffix}"
        )
    
    with col2:
        st.markdown("#### 👥 Asignación de Personal")
        # Usuario que reporta
        opciones_usuarios = [f"{usuario['_id']}" for usuario in usuarios_lista]
        nombres_usuarios = [f"{usuario['nombre']} ({usuario['rol']})" for usuario in usuarios_lista]
        
        indice_reporta = 0
        if falla and falla.get("usuario_reporta"):
            try:
                for i, usuario in enumerate(usuarios_lista):
                    if str(usuario["_id"]) == str(falla["usuario_reporta"]["_id"]):
                        indice_reporta = i
                        break
            except:
                indice_reporta = 0
        
        seleccion_reporta = st.selectbox(
            "📢 Usuario que reporta *",
            options=range(len(nombres_usuarios)),
            index=indice_reporta,
            format_func=lambda x: nombres_usuarios[x],
            key=f"reporta_{key_suffix}"
        )
        usuario_reporta_id = opciones_usuarios[seleccion_reporta] if usuarios_lista else None
        
        # Usuario que revisa - CORREGIDO: Definir variables fuera del if/else
        # Inicializar variables primero
        opciones_usuarios_revisa = opciones_usuarios.copy()
        nombres_usuarios_revisa = nombres_usuarios.copy()
        indice_revisa = 0
        
        if falla and falla.get("usuario_revisa"):
            try:
                for i, usuario in enumerate(usuarios_lista):
                    if str(usuario["_id"]) == str(falla["usuario_revisa"]["_id"]):
                        indice_revisa = i
                        break
            except:
                indice_revisa = 0
        else:
            # Agregar opción "No asignado" al principio
            opciones_usuarios_revisa = [""] + opciones_usuarios
            nombres_usuarios_revisa = ["No asignado"] + nombres_usuarios
            indice_revisa = 0
        
        seleccion_revisa = st.selectbox(
            "🔍 Usuario que revisa",
            options=range(len(nombres_usuarios_revisa)),
            index=indice_revisa,
            format_func=lambda x: nombres_usuarios_revisa[x],
            key=f"revisa_{key_suffix}"
        )
        usuario_revisa_id = opciones_usuarios_revisa[seleccion_revisa] if seleccion_revisa > 0 else None
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Descripción y observaciones
    st.markdown("#### 📝 Descripción de la Falla")
    descripcion = st.text_area(
        "❓ Descripción de la falla *",
        value=falla["descripcion"] if falla else "",
        height=100,
        placeholder="Describe detalladamente la falla encontrada...",
        key=f"descripcion_{key_suffix}"
    )
    
    observaciones = st.text_area(
        "💡 Observaciones / Solución aplicada",
        value=falla["observaciones"] if falla else "",
        height=100,
        placeholder="Describe las observaciones y solución aplicada...",
        key=f"observaciones_{key_suffix}"
    )
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Información adicional - CON DROPDOWNS
    st.markdown("#### ✅ Autorizaciones y Notificaciones")
    col3, col4 = st.columns(2)
    
    with col3:
        # Revisó por (dropdown)
        opciones_reviso = [f"{usuario['_id']}" for usuario in usuarios_lista]
        nombres_reviso = [f"{usuario['nombre']} ({usuario['correo']})" for usuario in usuarios_lista]
        
        indice_reviso = 0
        if falla and falla.get("reviso_por"):
            try:
                for i, usuario in enumerate(usuarios_lista):
                    if str(usuario["_id"]) == str(falla["reviso_por"]["_id"]):
                        indice_reviso = i
                        break
            except:
                indice_reviso = 0
        
        seleccion_reviso = st.selectbox(
            "👁️ Revisó por *",
            options=range(len(nombres_reviso)),
            index=indice_reviso,
            format_func=lambda x: nombres_reviso[x],
            key=f"reviso_{key_suffix}"
        )
        reviso_por_id = opciones_reviso[seleccion_reviso] if usuarios_lista else None
        
        # Autorizado por (dropdown)
        indice_autorizado = 0
        if falla and falla.get("autorizado_por"):
            try:
                for i, usuario in enumerate(usuarios_lista):
                    if str(usuario["_id"]) == str(falla["autorizado_por"]["_id"]):
                        indice_autorizado = i
                        break
            except:
                indice_autorizado = 0
        
        seleccion_autorizado = st.selectbox(
            "📝 Autorizado por *",
            options=range(len(nombres_reviso)),
            index=indice_autorizado,
            format_func=lambda x: nombres_reviso[x],
            key=f"autorizado_{key_suffix}"
        )
        autorizado_por_id = opciones_reviso[seleccion_autorizado] if usuarios_lista else None
    
    with col4:
        # Correo destino (dropdown con correos de usuarios)
        correos_usuarios = [usuario['correo'] for usuario in usuarios_lista]
        
        indice_correo = 0
        if falla and falla.get("correo_destino"):
            try:
                for i, correo in enumerate(correos_usuarios):
                    if correo == falla["correo_destino"]:
                        indice_correo = i
                        break
            except:
                indice_correo = 0
        
        # También permitir correo personalizado
        correo_seleccionado = st.selectbox(
            "📧 Correo destino *",
            options=correos_usuarios,
            index=indice_correo,
            key=f"correo_select_{key_suffix}"
        )
        
        # Campo adicional para correo personalizado si no está en la lista
        correo_personalizado = st.text_input(
            "📨 O ingresa un correo personalizado:",
            value="" if falla and falla.get("correo_destino") in correos_usuarios else (falla["correo_destino"] if falla else ""),
            placeholder="correo@ejemplo.com",
            key=f"correo_personal_{key_suffix}"
        )
        
        # Usar correo personalizado si se ingresó, de lo contrario usar el seleccionado
        correo_destino = correo_personalizado if correo_personalizado else correo_seleccionado
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Materiales usados
    st.markdown("#### 📦 Materiales Utilizados")
    st.markdown("Agrega los materiales utilizados en la reparación:")
    
    if not falla or "materiales_usados" not in falla:
        falla_materiales = []
    else:
        falla_materiales = falla["materiales_usados"]
    
    materiales_usados = []
    
    for i, material in enumerate(falla_materiales + [{}]):  # Agregar uno vacío para nuevo material
        with st.container(border=True):
            col_m1, col_m2, col_m3 = st.columns([3, 2, 1])
            
            with col_m1:
                # Seleccionar material
                opciones_materiales = [f"{mat['_id']}" for mat in materiales_lista]
                nombres_materiales = [f"{mat['clave_material']} - {mat['descripcion']} (Existencia: {mat['existencia']})" for mat in materiales_lista]
                
                indice_material = 0
                if material and material.get("material_id"):
                    try:
                        for j, mat in enumerate(materiales_lista):
                            if str(mat["_id"]) == str(material["material_id"]):
                                indice_material = j
                                break
                    except:
                        indice_material = 0
                
                seleccion_material = st.selectbox(
                    f"🔧 Material {i+1}",
                    options=range(len(nombres_materiales)),
                    index=indice_material,
                    key=f"material_{key_suffix}_{i}",
                    format_func=lambda x: nombres_materiales[x]
                )
                material_id = opciones_materiales[seleccion_material] if materiales_lista else None
            
            with col_m2:
                cantidad = st.number_input(
                    "📊 Cantidad",
                    min_value=0.0,
                    value=float(material.get("cantidad", 0)) if material else 0.0,
                    step=1.0,
                    key=f"cantidad_{key_suffix}_{i}"
                )
            
            with col_m3:
                if i < len(falla_materiales):
                    if st.button("❌", key=f"remove_{key_suffix}_{i}"):
                        # Eliminar este material de la lista
                        falla_materiales.pop(i)
                        st.rerun()
            
            if material_id and cantidad > 0:
                materiales_usados.append({
                    "material_id": material_id,
                    "cantidad": cantidad
                })
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Información del vehículo (opcional)
    st.markdown("#### 🚗 Información del Vehículo (Opcional)")
    
    col_v1, col_v2, col_v3 = st.columns(3)
    
    with col_v1:
        vehiculo_marca = st.text_input(
            "🏷️ Marca",
            value=falla["vehiculo"].get("marca") if falla and falla.get("vehiculo") else "",
            placeholder="Ej: Toyota",
            key=f"vehiculo_marca_{key_suffix}"
        )
    
    with col_v2:
        vehiculo_modelo = st.text_input(
            "🚙 Modelo",
            value=falla["vehiculo"].get("modelo") if falla and falla.get("vehiculo") else "",
            placeholder="Ej: Corolla",
            key=f"vehiculo_modelo_{key_suffix}"
        )
    
    with col_v3:
        vehiculo_placa = st.text_input(
            "🔢 Placa",
            value=falla["vehiculo"].get("placa") if falla and falla.get("vehiculo") else "",
            placeholder="Ej: ABC-123",
            key=f"vehiculo_placa_{key_suffix}"
        )
    
    vehiculo_data = {}
    if vehiculo_marca:
        vehiculo_data["marca"] = vehiculo_marca
    if vehiculo_modelo:
        vehiculo_data["modelo"] = vehiculo_modelo
    if vehiculo_placa:
        vehiculo_data["placa"] = vehiculo_placa
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return (
        lugar_id, usuario_reporta_id, usuario_revisa_id, fecha,
        nombre_conductor, descripcion, observaciones, reviso_por_id,
        materiales_usados, autorizado_por_id, correo_destino, vehiculo_data
    )

# CRUD PRINCIPAL
def crud_fallas():
    
    # Aplicar estilos personalizados
    aplicar_estilos()
    
    #  HEADER PRINCIPAL
    st.markdown("""
        <div class="header-principal">
            <h1>🔧 Gestión de Fallas y Reportes</h1>
            <p>Administra reportes de fallas y mantenimiento de manera eficiente</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 🔹 INICIALIZAR ESTADO PARA MENSAJES
    if "mensaje" not in st.session_state:
        st.session_state.mensaje = None
    if "tipo_mensaje" not in st.session_state:
        st.session_state.tipo_mensaje = None
    
    # 🔹 MOSTRAR MENSAJES EXISTENTES
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

    # 📊 SELECTOR DE ACCIÓN CON TABS
    tab1, tab2 = st.tabs(["➕ Crear Reporte de Falla", "📋 Gestionar Fallas"])

    # ---------------------------------------------------
    #  🔹 CREAR FALLA
    # ---------------------------------------------------
    with tab1:
        st.markdown("### ✨ Registrar nueva falla")
        st.markdown("Completa el formulario para reportar una nueva falla o incidente.")
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # USAR KEY ÚNICA PARA CREACIÓN
        (lugar_id, usuario_reporta_id, usuario_revisa_id, fecha,
         nombre_conductor, descripcion, observaciones, reviso_por_id,
         materiales_usados, autorizado_por_id, correo_destino, vehiculo) = formulario_falla(key_suffix="create")

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("✨ Crear reporte de falla", type="primary", use_container_width=True, key="btn_crear_falla"):
                if not all([lugar_id, usuario_reporta_id, fecha, nombre_conductor, descripcion, reviso_por_id, autorizado_por_id, correo_destino]):
                    st.session_state.mensaje = "Por favor completa todos los campos obligatorios (*)"
                    st.session_state.tipo_mensaje = "warning"
                    st.rerun()

                resp = create_falla_controller(
                    lugar_id=lugar_id,
                    usuario_reporta_id=usuario_reporta_id,
                    usuario_revisa_id=usuario_revisa_id,
                    fecha=fecha,
                    nombre_conductor=nombre_conductor,
                    descripcion=descripcion,
                    observaciones=observaciones,
                    reviso_por_id=reviso_por_id,
                    materiales_usados=materiales_usados,
                    autorizado_por_id=autorizado_por_id,
                    correo_destino=correo_destino,
                    vehiculo=vehiculo
                )

                if "error" in resp:
                    st.session_state.mensaje = resp["error"]
                    st.session_state.tipo_mensaje = "error"
                    st.rerun()
                else:
                    st.session_state.mensaje = "Falla registrada exitosamente."
                    st.session_state.tipo_mensaje = "success"
                    st.rerun()

    # ---------------------------------------------------
    #  🔹 LISTAR / EDITAR / ELIMINAR
    # ---------------------------------------------------
    with tab2:
        # 🔍 SECCIÓN DE BÚSQUEDA Y FILTROS
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 Búsqueda y Filtros")
        
        # Búsqueda rápida destacada
        busqueda_rapida = st.text_input(
            "⚡ Búsqueda rápida",
            placeholder="🔎 Busca por descripción, conductor, observaciones...",
            key="busqueda_rapida_fallas",
            label_visibility="collapsed"
        )
        
        with st.expander("🎛️ Filtros avanzados", expanded=False):
            col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
            
            with col_filtro1:
                filtro_lugar = st.text_input(
                    "🏢 Lugar",
                    placeholder="Filtrar por lugar",
                    key="filtro_lugar_fallas"
                )
            
            with col_filtro2:
                filtro_descripcion = st.text_input(
                    "📝 Descripción",
                    placeholder="Filtrar por descripción",
                    key="filtro_descripcion_fallas"
                )
            
            with col_filtro3:
                filtro_conductor = st.text_input(
                    "👤 Conductor",
                    placeholder="Filtrar por conductor",
                    key="filtro_conductor_fallas"
                )

            col_filtro4, col_filtro5 = st.columns(2)
            with col_filtro4:
                fecha_desde = st.date_input(
                    "📅 Fecha desde",
                    key="fecha_desde_fallas"
                )
            with col_filtro5:
                fecha_hasta = st.date_input(
                    "📅 Fecha hasta",
                    key="fecha_hasta_fallas"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 🔹 CONFIGURACIÓN DE PAGINACIÓN
        col_config1, col_config2, col_config3, col_config4 = st.columns([1, 1, 1, 1])
        
        with col_config1:
            por_pagina = st.selectbox(
                "📄 Por página",
                [5, 10, 20, 50],
                index=1,
                key="por_pagina_fallas"
            )
        
        # Determinar modo de búsqueda
        if busqueda_rapida:
            lista = buscar_fallas(busqueda_rapida)
            total_fallas = len(lista)
            total_paginas = 1
            pagina_actual = 1
            
            st.markdown(f"""
                <div class="pagination-info">
                    🔍 {total_fallas} fallas encontradas para "{busqueda_rapida}"
                </div>
            """, unsafe_allow_html=True)
            
        else:
            if "pagina_actual_fallas" not in st.session_state:
                st.session_state.pagina_actual_fallas = 1
            
            with col_config2:
                if st.button("⬅️ Anterior", key="btn_anterior_fallas", disabled=st.session_state.get("pagina_actual_fallas", 1) <= 1):
                    st.session_state.pagina_actual_fallas -= 1
                    st.rerun()
            
            with col_config3:
                resultado = get_fallas_paginadas(
                    filtro_lugar=filtro_lugar,
                    filtro_descripcion=filtro_descripcion,
                    filtro_conductor=filtro_conductor,
                    fecha_desde=fecha_desde.strftime("%Y-%m-%d") if fecha_desde else None,
                    fecha_hasta=fecha_hasta.strftime("%Y-%m-%d") if fecha_hasta else None,
                    pagina=st.session_state.pagina_actual_fallas,
                    por_pagina=por_pagina
                )
                
                lista = resultado["fallas"]
                total_fallas = resultado["total"]
                total_paginas = resultado["total_paginas"]
                pagina_actual = resultado["pagina"]
                
                if st.button("➡️ Siguiente", key="btn_siguiente_fallas", disabled=pagina_actual >= total_paginas):
                    st.session_state.pagina_actual_fallas += 1
                    st.rerun()
            
            with col_config4:
                # CORREGIDO: st.metric no acepta key, solo label, value, delta
                st.metric("Total", total_fallas)
            
            st.markdown(f"""
                <div class="pagination-info">
                    📄 Página {pagina_actual} de {total_paginas}
                </div>
            """, unsafe_allow_html=True)
            
            if pagina_actual > total_paginas and total_paginas > 0:
                st.session_state.pagina_actual_fallas = total_paginas
                st.rerun()

        if not lista:
            st.markdown("""
                <div class="info-box">
                    <h3 style="margin:0;">📭 No hay fallas reportadas</h3>
                    <p style="margin:0.5rem 0 0 0;">No se encontraron fallas que coincidan con los filtros aplicados.</p>
                </div>
            """, unsafe_allow_html=True)
            
        else:
            # 🔹 MOSTRAR FALLAS EN CARDS
            st.markdown("### 📋 Reportes de Fallas")
            
            for falla in lista:
                # Determinar badge según estado
                tiene_revision = falla.get('usuario_revisa') is not None
                badge_class = "badge-completado" if tiene_revision else "badge-pendiente"
                badge_text = "COMPLETADO" if tiene_revision else "PENDIENTE"

                with st.expander(
    f"📅 {falla['fecha'].strftime('%Y-%m-%d')} • {falla['descripcion'][:50]}...",
    expanded=False
):

                    st.markdown(f"""
                        <div style="text-align: right;">
                            <span class="{badge_class}">{badge_text}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.markdown("#### 📍 Información General")
                        st.write(f"**🏢 Lugar:** {falla.get('lugar_nombre', 'N/A')}")
                        st.write(f"**👤 Conductor:** {falla['nombre_conductor']}")
                        st.write(f"**📝 Descripción:** {falla['descripcion']}")
                        st.write(f"**💡 Observaciones:** {falla.get('observaciones', 'N/A')}")
                        
                        if falla.get('vehiculo') and (falla['vehiculo'].get('marca') or falla['vehiculo'].get('modelo') or falla['vehiculo'].get('placa')):
                            st.markdown("#### 🚗 Información del Vehículo")
                            if falla['vehiculo'].get('marca'):
                                st.write(f"**🏷️ Marca:** {falla['vehiculo']['marca']}")
                            if falla['vehiculo'].get('modelo'):
                                st.write(f"**🚙 Modelo:** {falla['vehiculo']['modelo']}")
                            if falla['vehiculo'].get('placa'):
                                st.write(f"**🔢 Placa:** {falla['vehiculo']['placa']}")
                    
                    with col_info2:
                        st.markdown("#### 👥 Personal Involucrado")
                        st.write(f"**📢 Reportado por:** {falla['usuario_reporta']['nombre']}")
                        if falla.get('usuario_revisa'):
                            st.write(f"**🔍 Revisado por:** {falla['usuario_revisa']['nombre']}")
                        if falla.get('reviso_por'):
                            st.write(f"**👁️ Revisó por:** {falla['reviso_por']['nombre']}")
                        if falla.get('autorizado_por'):
                            st.write(f"**📝 Autorizado por:** {falla['autorizado_por']['nombre']}")
                        st.write(f"**📧 Correo destino:** {falla.get('correo_destino', 'N/A')}")
                        
                        if falla.get('materiales_usados'):
                            st.markdown("#### 📦 Materiales Utilizados")
                            for material in falla['materiales_usados']:
                                if material.get('material_info'):
                                    st.markdown(f"""
                                        <div class="material-item">
                                            <strong>{material['material_info']['descripcion']}</strong><br>
                                            Cantidad: {material['cantidad']}
                                        </div>
                                    """, unsafe_allow_html=True)
                    
                    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                    
                    st.markdown("#### ✏️ Editar información")
                    
                    # USAR KEY ÚNICA PARA CADA FALLA EN EDICIÓN
                    (lugar_id, usuario_reporta_id, usuario_revisa_id, fecha,
                     nombre_conductor, descripcion, observaciones, reviso_por_id,
                     materiales_usados, autorizado_por_id, correo_destino, vehiculo) = formulario_falla(
                        falla=falla, 
                        key_suffix=f"edit_{falla['_id']}"
                    )
                    
                    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                    
                    col_btn1, col_btn2, col_btn3 = st.columns(3)
                    
                    with col_btn1:
                        if st.button(
                            "💾 Guardar cambios", 
                            key=f"save_{falla['_id']}",
                            type="primary",
                            use_container_width=True
                        ):
                            if not all([lugar_id, usuario_reporta_id, fecha, nombre_conductor, descripcion, reviso_por_id, autorizado_por_id, correo_destino]):
                                st.session_state.mensaje = "Todos los campos obligatorios son requeridos."
                                st.session_state.tipo_mensaje = "warning"
                                st.rerun()
                            
                            try:
                                resultado = update_falla(
                                    falla["_id"],
                                    lugar_id,
                                    usuario_reporta_id,
                                    usuario_revisa_id,
                                    fecha,
                                    nombre_conductor,
                                    descripcion,
                                    observaciones,
                                    reviso_por_id,
                                    materiales_usados,
                                    autorizado_por_id,
                                    correo_destino,
                                    vehiculo
                                )
                                
                                if "error" in resultado:
                                    st.session_state.mensaje = resultado["error"]
                                    st.session_state.tipo_mensaje = "error"
                                else:
                                    st.session_state.mensaje = "Falla actualizada exitosamente."
                                    st.session_state.tipo_mensaje = "success"
                                st.rerun()
                            except Exception as e:
                                st.session_state.mensaje = f"Error: {str(e)}"
                                st.session_state.tipo_mensaje = "error"
                                st.rerun()

                    with col_btn2:
                        if st.button(
                            "🗑️ Eliminar", 
                            key=f"delete_{falla['_id']}",
                            use_container_width=True
                        ):
                            try:
                                delete_falla(falla["_id"])
                                st.session_state.mensaje = "Falla eliminada correctamente."
                                st.session_state.tipo_mensaje = "success"
                                st.rerun()
                            except Exception as e:
                                st.session_state.mensaje = f"Error: {str(e)}"
                                st.session_state.tipo_mensaje = "error"
                                st.rerun()
                    
                    with col_btn3:
                        if st.button(
                            "🔄 Restablecer", 
                            key=f"reset_{falla['_id']}",
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
                        key="btn_anterior_inf_fallas", 
                        use_container_width=True,
                        disabled=pagina_actual <= 1
                    ):
                        st.session_state.pagina_actual_fallas -= 1
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
                        key="btn_siguiente_inf_fallas", 
                        use_container_width=True,
                        disabled=pagina_actual >= total_paginas
                    ):
                        st.session_state.pagina_actual_fallas += 1
                        st.rerun()

    # ================================
    # EDITAR FALLA (MODO ANTIGUO - como respaldo)
    # ================================
    if "editar_falla_id" in st.session_state:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### ✏️ Edición Rápida de Falla")
        
        falla_id = st.session_state["editar_falla_id"]
        falla = get_falla_by_id(falla_id)

        if not falla:
            st.error("❌ Falla no encontrada.")
            del st.session_state["editar_falla_id"]
            st.rerun()

        (lugar_id, usuario_reporta_id, usuario_revisa_id, fecha,
         nombre_conductor, descripcion, observaciones, reviso_por_id,
         materiales_usados, autorizado_por_id, correo_destino, vehiculo) = formulario_falla(
            falla=falla, 
            key_suffix=f"quick_edit_{falla_id}"
        )

        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Actualizar falla", type="primary", use_container_width=True, key=f"quick_save_{falla_id}"):
                resultado = update_falla(
                    falla_id,
                    lugar_id,
                    usuario_reporta_id,
                    usuario_revisa_id,
                    fecha,
                    nombre_conductor,
                    descripcion,
                    observaciones,
                    reviso_por_id,
                    materiales_usados,
                    autorizado_por_id,
                    correo_destino,
                    vehiculo
                )
                if "error" in resultado:
                    st.session_state.mensaje = resultado["error"]
                    st.session_state.tipo_mensaje = "error"
                else:
                    st.session_state.mensaje = "Falla actualizada exitosamente."
                    st.session_state.tipo_mensaje = "success"
                    del st.session_state["editar_falla_id"]
                st.rerun()
        
        with col2:
            if st.button("❌ Cancelar edición", use_container_width=True, key=f"quick_cancel_{falla_id}"):
                del st.session_state["editar_falla_id"]
                st.rerun()