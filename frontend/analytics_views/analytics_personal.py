import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.controllers.usuarios_controller import get_all_usuarios
from backend.controllers.fallas_controller import get_all_fallas

def mostrar_analytics_personal():
    # ESTILOS CSS PERSONALIZADOS
    st.markdown("""
        <style>
        /* Estilos globales */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header principal */
        .header-analytics {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-analytics h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-analytics p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }
        
        /* Info boxes */
        .info-analytics {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Help box */
        .help-box-analytics {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .help-box-analytics h3 {
            margin-top: 0;
        }
        
        /* Section container */
        .section-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin-bottom: 1.5rem;
        }
        
        /* Metric card */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        /* Divider */
        .divider-analytics {
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 2rem 0;
        }
        
        /* Recommendation card */
        .recommendation-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            border-left: 4px solid #ff9a56;
        }
        
        .recommendation-card h4 {
            margin-top: 0;
            color: #333;
        }
        
        /* Warning card */
        .warning-card {
            background: linear-gradient(135deg, #f093fb15 0%, #f5576c15 100%);
            border-left: 4px solid #f5576c;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Success card */
        .success-card {
            background: linear-gradient(135deg, #84fab015 0%, #8fd3f415 100%);
            border-left: 4px solid #84fab0;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Table help */
        .table-help {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .table-help h4 {
            margin-top: 0;
            color: #333;
        }
        
        /* Chart container */
        .chart-container {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        </style>
    """, unsafe_allow_html=True)
    
    #  HEADER PRINCIPAL
    st.markdown("""
        <div class="header-analytics">
            <h1>👥 Analytics de Personal</h1>
            <p>Análisis inteligente de rendimiento y asignaciones del equipo</p>
        </div>
    """, unsafe_allow_html=True)
    
    #  AYUDA GENERAL
    with st.expander("📖 ¿Cómo interpretar estos datos?", expanded=False):
        st.markdown("""
            <div class="help-box-analytics">
                <h3>🎯 Guía de Analytics de Personal</h3>
                <p><strong>Este módulo te ayuda a:</strong></p>
                <ul>
                    <li>📊 <strong>Visualizar métricas del equipo:</strong> Total de usuarios, distribución por roles</li>
                    <li>📈 <strong>Analizar actividad:</strong> Quiénes son los usuarios más activos en reportes</li>
                    <li>🤖 <strong>Obtener recomendaciones:</strong> Sugerencias basadas en IA para optimizar tu equipo</li>
                    <li>👨‍💼 <strong>Gestionar personal:</strong> Lista completa con información de contacto</li>
                </ul>
                <p style="margin-top: 1rem;"><strong>💡 Consejo:</strong> Revisa regularmente estos datos para identificar oportunidades de mejora en tu equipo.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Cargar datos
    usuarios = get_all_usuarios()
    fallas = get_all_fallas()
    df_usuarios = pd.DataFrame(usuarios)
    df_fallas = pd.DataFrame(fallas)
    
    if df_usuarios.empty:
        st.markdown("""
            <div class="warning-card">
                <h3 style="margin:0;">⚠️ No hay datos disponibles</h3>
                <p style="margin:0.5rem 0 0 0;">No se encontraron usuarios registrados en el sistema. Comienza agregando personal en el módulo de Gestión de Usuarios.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # SECCIÓN 1: MÉTRICAS DEL EQUIPO
    st.markdown("### 📊 Métricas Generales del Equipo")
    
    st.markdown("""
        <div class="info-analytics">
            <strong>ℹ️ Acerca de estas métricas:</strong> Estas cifras te dan una vista rápida del tamaño y composición de tu equipo.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_usuarios = len(df_usuarios)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">👥 TOTAL USUARIOS</div>
                <div class="metric-value">{total_usuarios}</div>
                <div class="metric-label">Miembros del equipo</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        admins = len(df_usuarios[df_usuarios['rol'] == 'admin'])
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <div class="metric-label">👑 ADMINISTRADORES</div>
                <div class="metric-value">{admins}</div>
                <div class="metric-label">Control total del sistema</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        empleados = len(df_usuarios[df_usuarios['rol'] == 'empleado'])
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">👤 EMPLEADOS</div>
                <div class="metric-value">{empleados}</div>
                <div class="metric-label">Personal operativo</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-analytics"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 2: DISTRIBUCIÓN POR ROL
    st.markdown("### 📋 Distribución del Personal")
    
    st.markdown("""
        <div class="table-help">
            <h4>📌 Interpretación del gráfico</h4>
            <p><strong>¿Qué muestra?</strong> Este gráfico de pastel visualiza el porcentaje de administradores vs empleados en tu organización.</p>
            <p><strong>Recomendación:</strong> Una proporción saludable es 20-30% administradores y 70-80% empleados operativos.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    
    distribucion_roles = df_usuarios['rol'].value_counts()
    
    # Crear gráfico mejorado
    colors = ['#667eea', '#4facfe']
    fig = go.Figure(data=[go.Pie(
        labels=['👑 Administradores' if x == 'admin' else '👤 Empleados' for x in distribucion_roles.index],
        values=distribucion_roles.values,
        hole=.4,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textfont=dict(size=14)
    )])
    
    fig.update_layout(
        title={
            'text': "Distribución por Rol",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#333'}
        },
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Análisis de la distribución
    porcentaje_admin = (admins / total_usuarios) * 100
    
    if porcentaje_admin > 50:
        st.markdown("""
            <div class="warning-card">
                <strong>⚠️ Alerta:</strong> Tienes un alto porcentaje de administradores ({:.1f}%). 
                Considera reasignar roles para optimizar la estructura organizacional.
            </div>
        """.format(porcentaje_admin), unsafe_allow_html=True)
    elif porcentaje_admin < 20:
        st.markdown("""
            <div class="info-analytics">
                <strong>ℹ️ Observación:</strong> Tienes un bajo porcentaje de administradores ({:.1f}%). 
                Asegúrate de tener suficiente personal con permisos administrativos.
            </div>
        """.format(porcentaje_admin), unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="success-card">
                <strong>✅ Excelente:</strong> Tu distribución de roles es equilibrada ({:.1f}% administradores).
            </div>
        """.format(porcentaje_admin), unsafe_allow_html=True)
    
    st.markdown('<div class="divider-analytics"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 3: ANÁLISIS DE ACTIVIDAD
    st.markdown("### 📊 Análisis de Actividad")
    
    st.markdown("""
        <div class="table-help">
            <h4>🔍 ¿Qué mide la actividad?</h4>
            <p><strong>Métrica:</strong> Este gráfico muestra qué usuarios han reportado más fallas en el sistema.</p>
            <p><strong>Utilidad:</strong> Identifica a los miembros más proactivos del equipo y detecta posibles áreas que requieren más atención.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_fallas.empty:
        if 'usuario_reporta' in df_fallas.columns:
            try:
                usuarios_reportes = df_fallas['usuario_reporta'].apply(
                    lambda x: x.get('nombre', 'N/A') if isinstance(x, dict) else 'N/A'
                )
                usuarios_activos = usuarios_reportes.value_counts().head(5)
                
                if not usuarios_activos.empty:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=usuarios_activos.index,
                            y=usuarios_activos.values,
                            marker=dict(
                                color=usuarios_activos.values,
                                colorscale='Viridis',
                                showscale=True,
                                colorbar=dict(title="Reportes")
                            ),
                            text=usuarios_activos.values,
                            textposition='auto',
                        )
                    ])
                    
                    fig.update_layout(
                        title={
                            'text': "Top 5 Usuarios Más Activos en Reportes",
                            'x': 0.5,
                            'xanchor': 'center',
                            'font': {'size': 20, 'color': '#333'}
                        },
                        xaxis_title="Usuario",
                        yaxis_title="Número de Reportes",
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Análisis de actividad
                    usuario_mas_activo = usuarios_activos.index[0]
                    reportes_max = usuarios_activos.values[0]
                    
                    st.markdown(f"""
                        <div class="success-card">
                            <strong>🏆 Usuario Destacado:</strong> {usuario_mas_activo} lidera con {reportes_max} reportes.
                            Este nivel de proactividad es excelente para el mantenimiento preventivo.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="info-analytics">
                            <strong>ℹ️ Sin reportes:</strong> Aún no hay usuarios con reportes de fallas registrados.
                        </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown("""
                    <div class="warning-card">
                        <strong>⚠️ Error:</strong> No se pudo analizar la actividad de usuarios. 
                        Verifica que los reportes tengan el formato correcto.
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="info-analytics">
                <strong>ℹ️ Sin datos de fallas:</strong> No hay reportes de fallas registrados en el sistema.
                Una vez que se registren fallas, podrás ver la actividad de los usuarios aquí.
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-analytics"></div>', unsafe_allow_html=True)
    
    
    # SECCIÓN 4: RECOMENDACIONES IA
    st.markdown("### 🤖 Recomendaciones Inteligentes")
    
    st.markdown("""
        <div class="table-help">
            <h4>🧠 IA Analytics</h4>
            <p><strong>¿Qué son estas recomendaciones?</strong> Basadas en el análisis de datos de tu equipo, el sistema genera sugerencias automáticas para optimizar la gestión del personal.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
            <div class="recommendation-card">
                <h4>🎯 Optimización de Roles</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("**Análisis basado en los datos del sistema:**")
        
        if len(df_usuarios[df_usuarios['rol'] == 'admin']) / len(df_usuarios) > 0.5:
            st.markdown("""
                <div class="warning-card">
                    <strong>⚠️ Recomendación:</strong> Considera convertir algunos administradores a empleados para mejor distribución.
                    <br><br>
                    <strong>Beneficios:</strong>
                    <ul>
                        <li>Mejora la seguridad del sistema</li>
                        <li>Reduce riesgo de cambios accidentales</li>
                        <li>Establece jerarquías más claras</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="success-card">
                    <strong>✅ Estado Óptimo:</strong> Distribución de roles equilibrada.
                    <br><br>
                    Tu estructura actual permite un buen balance entre control administrativo y operaciones.
                </div>
            """, unsafe_allow_html=True)
    
    with col_rec2:
        st.markdown("""
            <div class="recommendation-card">
                <h4>📈 Oportunidades de Capacitación</h4>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("**Áreas identificadas para desarrollo:**")
        
        capacitaciones = []
        
        if df_fallas.empty or len(df_fallas) < total_usuarios * 2:
            capacitaciones.append("🎓 **Reporte de fallas:** Capacitar al equipo en procedimientos de reporte")
        
        if not df_fallas.empty and 'usuario_reporta' in df_fallas.columns:
            usuarios_sin_reportes = set(df_usuarios['nombre']) - set(
                df_fallas['usuario_reporta'].apply(lambda x: x.get('nombre', '') if isinstance(x, dict) else '')
            )
            if len(usuarios_sin_reportes) > total_usuarios * 0.3:
                capacitaciones.append("👥 **Participación activa:** Incentivar el uso del sistema")
        
        capacitaciones.append("🔧 **Uso del sistema de inventario:** Mejorar gestión de materiales")
        capacitaciones.append("📋 **Procedimientos de mantenimiento:** Estandarizar procesos")
        
        for cap in capacitaciones:
            st.markdown(f"""
                <div class="info-analytics">
                    {cap}
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-analytics"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 5: LISTA DE PERSONAL
    st.markdown("### 👨‍💼 Lista Completa de Personal")
    
    st.markdown("""
        <div class="table-help">
            <h4>📋 Tabla de Personal</h4>
            <p><strong>¿Qué muestra?</strong> Directorio completo de todos los usuarios registrados en el sistema.</p>
            <p><strong>Información incluida:</strong></p>
            <ul>
                <li><strong>Nombre:</strong> Identificación del usuario</li>
                <li><strong>Correo:</strong> Email de contacto corporativo</li>
                <li><strong>Rol:</strong> Nivel de permisos en el sistema (admin/empleado)</li>
            </ul>
            <p><strong>💡 Tip:</strong> Puedes ordenar la tabla haciendo clic en los encabezados de columna.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_usuarios.empty:
        st.markdown('<div class="section-container">', unsafe_allow_html=True)
        
        # Crear vista mejorada para la tabla
        vista_usuarios = df_usuarios[['nombre', 'correo', 'rol']].copy()
        vista_usuarios.columns = ['👤 Nombre', '📧 Correo Electrónico', '🎭 Rol']
        
        # Reemplazar valores de rol con emojis
        vista_usuarios['🎭 Rol'] = vista_usuarios['🎭 Rol'].replace({
            'admin': '👑 Administrador',
            'empleado': '👤 Empleado'
        })
        
        st.dataframe(
            vista_usuarios,
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Estadísticas adicionales
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.markdown("""
                <div class="info-analytics" style="text-align: center;">
                    <strong>📊 Total Registros</strong><br>
                    <span style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{}</span>
                </div>
            """.format(len(vista_usuarios)), unsafe_allow_html=True)
        
        with col_stat2:
            correos_validos = len([c for c in vista_usuarios['📧 Correo Electrónico'] if '@' in str(c)])
            st.markdown("""
                <div class="info-analytics" style="text-align: center;">
                    <strong>✉️ Correos Válidos</strong><br>
                    <span style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{}</span>
                </div>
            """.format(correos_validos), unsafe_allow_html=True)
        
        with col_stat3:
            porcentaje_completo = (correos_validos / len(vista_usuarios)) * 100
            st.markdown("""
                <div class="info-analytics" style="text-align: center;">
                    <strong>📈 Datos Completos</strong><br>
                    <span style="font-size: 1.5rem; font-weight: 700; color: #667eea;">{:.0f}%</span>
                </div>
            """.format(porcentaje_completo), unsafe_allow_html=True)