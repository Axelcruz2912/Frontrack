import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.controllers.fallas_controller import get_all_fallas
from backend.controllers.materiales_controller import get_all_materiales
from backend.controllers.usuarios_controller import get_all_usuarios
from datetime import datetime

def mostrar_dashboard_principal():
    user = st.session_state.get("user", {})
    rol = user.get("rol", "empleado")
    es_admin = rol == "admin"

    #  ESTILOS CSS PERSONALIZADOS
    st.markdown("""
        <style>
        /* Estilos globales */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header principal */
        .header-dashboard {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-dashboard h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-dashboard p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }
        
        /* KPI Cards */
        .kpi-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            text-align: center;
            transition: all 0.3s ease;
            border-top: 4px solid;
        }
        
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        }
        
        .kpi-card-fallas {
            border-color: #f093fb;
        }
        
        .kpi-card-materiales {
            border-color: #fa709a;
        }
        
        .kpi-card-usuarios {
            border-color: #667eea;
        }
        
        .kpi-card-mes {
            border-color: #11998e;
        }
        
        .kpi-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .kpi-value {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .kpi-label {
            font-size: 0.9rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Help boxes */
        .help-dashboard {
            background: linear-gradient(135deg, #84fab015 0%, #8fd3f415 100%);
            border-left: 4px solid #84fab0;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .help-main {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
        }
        
        .help-main h3 {
            margin-top: 0;
            color: #333;
        }
        
        /* Chart container */
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin-bottom: 1.5rem;
        }
        
        /* Section header */
        .section-header {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            padding: 1rem 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            margin: 2rem 0 1rem 0;
        }
        
        .section-header h3 {
            margin: 0;
            color: #333;
        }
        
        /* Divider */
        .divider-dashboard {
            height: 2px;
            background: linear-gradient(90deg, transparent, #11998e, transparent);
            margin: 2rem 0;
        }
        
        /* Alert boxes */
        .alert-success {
            background: linear-gradient(135deg, #84fab015 0%, #8fd3f415 100%);
            border-left: 4px solid #84fab0;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        .alert-warning {
            background: linear-gradient(135deg, #f093fb15 0%, #f5576c15 100%);
            border-left: 4px solid #f5576c;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        .alert-info {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Restricted access message */
        .restricted-access {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border: 2px solid #f59e0b;
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
        }
        
        /* Stats badge */
        .stats-badge {
            display: inline-block;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0.2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    #  HEADER PRINCIPAL (Diferente según rol)
    if es_admin:
        st.markdown("""
            <div class="header-dashboard">
                <h1>📊 Dashboard Principal - Administrador</h1>
                <p>Vista completa del sistema de gestión en tiempo real</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="header-dashboard">
                <h1>📊 Dashboard de Fallas</h1>
                <p>Vista de fallas y reportes para empleados</p>
            </div>
        """, unsafe_allow_html=True)
    
    # AYUDA GENERAL
    with st.expander("📖 Guía del Dashboard", expanded=False):
        if es_admin:
            st.markdown("""
                <div class="help-main">
                    <h3>🎯 Dashboard Completo - Administrador</h3>
                    <p><strong>Tienes acceso a todas las funcionalidades:</strong></p>
                    <ul>
                        <li>📈 <strong>KPIs completos:</strong> Fallas, materiales, usuarios y tendencias</li>
                        <li>📊 <strong>Visualizaciones avanzadas:</strong> Análisis de stock y distribución</li>
                        <li>🔍 <strong>Tendencias temporales:</strong> Evolución completa del sistema</li>
                        <li>⚡ <strong>Resumen ejecutivo:</strong> Vista general para toma de decisiones</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="help-main">
                    <h3>🎯 Dashboard de Fallas - Empleado</h3>
                    <p><strong>Acceso limitado a información de fallas:</strong></p>
                    <ul>
                        <li>📈 <strong>KPIs básicos:</strong> Solo métricas relacionadas con fallas</li>
                        <li>📊 <strong>Gráfica de fallas:</strong> Top lugares con más reportes</li>
                        <li>🔍 <strong>Información esencial:</strong> Solo datos necesarios para tus tareas</li>
                    </ul>
                    <p style="margin-top: 1rem;"><strong>💡 Contacta al administrador</strong> si necesitas acceso a más información.</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Cargar datos con spinner mejorado
    with st.spinner("🔄 Cargando datos del sistema..."):
        fallas = get_all_fallas()
        materiales = get_all_materiales()
        usuarios = get_all_usuarios()
    
    # Convertir a DataFrames
    df_fallas = pd.DataFrame(fallas)
    df_materiales = pd.DataFrame(materiales)
    df_usuarios = pd.DataFrame(usuarios)
    
    # SECCIÓN 1: KPIs PRINCIPALES
    st.markdown("""
        <div class="section-header">
            <h3>📊 Indicadores Clave de Rendimiento</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if es_admin:
        st.markdown("""
            <div class="help-dashboard">
                <strong>ℹ️ KPIs Completos:</strong> Como administrador, ves todas las métricas del sistema.
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_fallas = len(df_fallas)
            st.markdown(f"""
                <div class="kpi-card kpi-card-fallas">
                    <div class="kpi-icon">🔧</div>
                    <div class="kpi-value" style="color: #f093fb;">{total_fallas}</div>
                    <div class="kpi-label">Fallas Registradas</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_materiales = len(df_materiales)
            st.markdown(f"""
                <div class="kpi-card kpi-card-materiales">
                    <div class="kpi-icon">📦</div>
                    <div class="kpi-value" style="color: #fa709a;">{total_materiales}</div>
                    <div class="kpi-label">Materiales en Inventario</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_usuarios = len(df_usuarios)
            st.markdown(f"""
                <div class="kpi-card kpi-card-usuarios">
                    <div class="kpi-icon">👥</div>
                    <div class="kpi-value" style="color: #667eea;">{total_usuarios}</div>
                    <div class="kpi-label">Usuarios Activos</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if not df_fallas.empty and 'fecha' in df_fallas.columns:
                df_fallas['fecha'] = pd.to_datetime(df_fallas['fecha'])
                mes_actual = pd.Timestamp.now().month
                fallas_este_mes = len(df_fallas[df_fallas['fecha'].dt.month == mes_actual])
            else:
                fallas_este_mes = 0
            
            st.markdown(f"""
                <div class="kpi-card kpi-card-mes">
                    <div class="kpi-icon">📅</div>
                    <div class="kpi-value" style="color: #11998e;">{fallas_este_mes}</div>
                    <div class="kpi-label">Fallas Este Mes</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="help-dashboard">
                <strong>ℹ️ KPIs Limitados:</strong> Como empleado, solo ves métricas relacionadas con fallas.
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_fallas = len(df_fallas)
            st.markdown(f"""
                <div class="kpi-card kpi-card-fallas">
                    <div class="kpi-icon">🔧</div>
                    <div class="kpi-value" style="color: #f093fb;">{total_fallas}</div>
                    <div class="kpi-label">Fallas Registradas</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if not df_fallas.empty and 'fecha' in df_fallas.columns:
                df_fallas['fecha'] = pd.to_datetime(df_fallas['fecha'])
                mes_actual = pd.Timestamp.now().month
                fallas_este_mes = len(df_fallas[df_fallas['fecha'].dt.month == mes_actual])
            else:
                fallas_este_mes = 0
            
            st.markdown(f"""
                <div class="kpi-card kpi-card-mes">
                    <div class="kpi-icon">📅</div>
                    <div class="kpi-value" style="color: #11998e;">{fallas_este_mes}</div>
                    <div class="kpi-label">Fallas Este Mes</div>
                </div>
            """, unsafe_allow_html=True)
    
    # Análisis de KPIs (solo para fallas)
    if total_fallas > 0:
        tasa_fallas_mes = (fallas_este_mes / total_fallas) * 100
        if tasa_fallas_mes > 50:
            st.markdown(f"""
                <div class="alert-warning">
                    <strong>⚠️ Alerta:</strong> El {tasa_fallas_mes:.1f}% de las fallas ocurrieron este mes. 
                    Se recomienda revisar los procesos de mantenimiento preventivo.
                </div>
            """, unsafe_allow_html=True)
        elif fallas_este_mes == 0:
            st.markdown("""
                <div class="alert-success">
                    <strong>✅ Excelente:</strong> No se han registrado fallas este mes. ¡Mantén las buenas prácticas!
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-dashboard"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 2: GRÁFICOS COMPARATIVOS
    st.markdown("""
        <div class="section-header">
            <h3>📈 Análisis Visual de Datos</h3>
        </div>
    """, unsafe_allow_html=True)
    
    if es_admin:
        # VISTA COMPLETA PARA ADMINISTRADORES
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("""
                <div class="help-dashboard">
                    <strong>📍 Top 5 Lugares con Más Fallas</strong><br>
                    <em>¿Qué muestra?</em> Identifica las ubicaciones que requieren mayor atención de mantenimiento.
                </div>
            """, unsafe_allow_html=True)
            
            if not df_fallas.empty and 'lugar_nombre' in df_fallas.columns:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                fallas_por_lugar = df_fallas['lugar_nombre'].value_counts().head(5)
                
                fig = go.Figure(data=[
                    go.Bar(
                        x=fallas_por_lugar.index,
                        y=fallas_por_lugar.values,
                        marker=dict(
                            color=fallas_por_lugar.values,
                            colorscale='Reds',
                            showscale=True,
                            colorbar=dict(title="Fallas")
                        ),
                        text=fallas_por_lugar.values,
                        textposition='auto',
                    )
                ])
                
                fig.update_layout(
                    title={
                        'text': "Top 5 Lugares con Más Fallas",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#333'}
                    },
                    xaxis_title="Lugar",
                    yaxis_title="Número de Fallas",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Análisis del lugar más crítico
                if not fallas_por_lugar.empty:
                    lugar_critico = fallas_por_lugar.index[0]
                    fallas_criticas = fallas_por_lugar.values[0]
                    st.markdown(f"""
                        <div class="alert-warning">
                            <strong>🎯 Lugar Crítico:</strong> {lugar_critico} con {fallas_criticas} fallas registradas.
                            Considera programar una inspección detallada.
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="alert-info">
                        <strong>ℹ️ Sin datos:</strong> No hay fallas registradas con información de lugares.
                    </div>
                """, unsafe_allow_html=True)
        
        with col_chart2:
            st.markdown("""
                <div class="help-dashboard">
                    <strong>📊 Distribución de Niveles de Stock</strong><br>
                    <em>¿Qué muestra?</em> Estado del inventario clasificado por nivel de existencias.
                </div>
            """, unsafe_allow_html=True)
            
            if not df_materiales.empty and 'existencia' in df_materiales.columns:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                
                # Clasificar materiales por nivel de stock
                df_materiales['nivel_stock'] = pd.cut(
                    df_materiales['existencia'], 
                    bins=[-1, 0, 5, 20, float('inf')],
                    labels=['🔴 Sin Stock', '🟡 Bajo', '🟢 Normal', '🔵 Alto']
                )
                stock_counts = df_materiales['nivel_stock'].value_counts()
                
                colors = ['#868f96', '#f5576c', '#84fab0', '#667eea']
                
                fig = go.Figure(data=[go.Pie(
                    labels=stock_counts.index,
                    values=stock_counts.values,
                    hole=.4,
                    marker=dict(colors=colors),
                    textinfo='label+percent+value',
                    textfont=dict(size=12)
                )])
                
                fig.update_layout(
                    title={
                        'text': "Distribución de Niveles de Stock",
                        'x': 0.5,
                        'xanchor': 'center',
                        'font': {'size': 18, 'color': '#333'}
                    },
                    showlegend=True,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Análisis de stock
                sin_stock = stock_counts.get('🔴 Sin Stock', 0)
                bajo_stock = stock_counts.get('🟡 Bajo', 0)
                
                if sin_stock > 0 or bajo_stock > 0:
                    st.markdown(f"""
                        <div class="alert-warning">
                            <strong>⚠️ Atención al Inventario:</strong><br>
                            • {sin_stock} materiales sin stock<br>
                            • {bajo_stock} materiales con stock bajo<br>
                            <em>Recomendación:</em> Programa un reabastecimiento.
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="alert-info">
                        <strong>ℹ️ Sin datos:</strong> No hay materiales en el inventario.
                    </div>
                """, unsafe_allow_html=True)
    
    else:
        # VISTA LIMITADA PARA EMPLEADOS - SOLO GRÁFICA DE FALLAS
        st.markdown("""
            <div class="help-dashboard">
                <strong>📍 Top Lugares con Más Fallas</strong><br>
                <em>¿Qué muestra?</em> Identifica las ubicaciones que requieren mayor atención de mantenimiento.<br>
                <em>Acción:</strong> Prioriza reportes y atención en los lugares con más incidencias.
            </div>
        """, unsafe_allow_html=True)
        
        if not df_fallas.empty and 'lugar_nombre' in df_fallas.columns:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fallas_por_lugar = df_fallas['lugar_nombre'].value_counts().head(5)
            
            fig = go.Figure(data=[
                go.Bar(
                    x=fallas_por_lugar.index,
                    y=fallas_por_lugar.values,
                    marker=dict(
                        color=fallas_por_lugar.values,
                        colorscale='Reds',
                        showscale=True,
                        colorbar=dict(title="Fallas")
                    ),
                    text=fallas_por_lugar.values,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title={
                    'text': "Top 5 Lugares con Más Fallas",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#333'}
                },
                xaxis_title="Lugar",
                yaxis_title="Número de Fallas",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Análisis del lugar más crítico
            if not fallas_por_lugar.empty:
                lugar_critico = fallas_por_lugar.index[0]
                fallas_criticas = fallas_por_lugar.values[0]
                st.markdown(f"""
                    <div class="alert-warning">
                        <strong>🎯 Lugar Crítico:</strong> {lugar_critico} con {fallas_criticas} fallas registradas.
                        Reporta cualquier anomalía que detectes en esta área.
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="alert-info">
                    <strong>ℹ️ Sin datos:</strong> No hay fallas registradas con información de lugares.
                    Una vez que se registren fallas con ubicación, verás el análisis aquí.
                </div>
            """, unsafe_allow_html=True)
        
        # Mensaje de acceso restringido para otras gráficas
        st.markdown("""
            <div class="restricted-access">
                <h3>🔒 Acceso Restringido</h3>
                <p>Como empleado, solo puedes ver información relacionada con fallas y reportes.</p>
                <p><strong>Información de inventario y usuarios está limitada a administradores.</strong></p>
                <p>💡 Contacta con un administrador si necesitas acceso a más información.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-dashboard"></div>', unsafe_allow_html=True)
    
    
    # SECCIÓN 3: TENDENCIAS TEMPORALES (SOLO ADMIN)
    if es_admin:
        st.markdown("""
            <div class="section-header">
                <h3>📈 Tendencias Temporales</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="help-dashboard">
                <strong>📅 Evolución de Fallas por Mes</strong><br>
                <em>¿Qué muestra?</em> Gráfico de línea que muestra cómo han evolucionado las fallas a lo largo del tiempo.
            </div>
        """, unsafe_allow_html=True)
        
        if not df_fallas.empty and 'fecha' in df_fallas.columns:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            df_fallas['fecha'] = pd.to_datetime(df_fallas['fecha'])
            df_fallas['mes'] = df_fallas['fecha'].dt.to_period('M').astype(str)
            tendencias_mensuales = df_fallas.groupby('mes').size().reset_index(name='fallas')
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=tendencias_mensuales['mes'],
                y=tendencias_mensuales['fallas'],
                mode='lines+markers',
                name='Fallas',
                line=dict(color='#f093fb', width=3),
                marker=dict(size=8, color='#f5576c'),
                fill='tozeroy',
                fillcolor='rgba(240, 147, 251, 0.2)'
            ))
            
            fig.update_layout(
                title={
                    'text': "Evolución de Fallas por Mes",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#333'}
                },
                xaxis_title="Mes",
                yaxis_title="Número de Fallas",
                height=400,
                showlegend=False,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Análisis de tendencia
            if len(tendencias_mensuales) >= 2:
                tendencia_reciente = tendencias_mensuales['fallas'].tail(2).tolist()
                if tendencia_reciente[1] > tendencia_reciente[0]:
                    diferencia = tendencia_reciente[1] - tendencia_reciente[0]
                    porcentaje = (diferencia / tendencia_reciente[0]) * 100
                    st.markdown(f"""
                        <div class="alert-warning">
                            <strong>📈 Tendencia al Alza:</strong> Las fallas aumentaron {diferencia} casos ({porcentaje:.1f}%) 
                            respecto al mes anterior. Revisa los procesos de mantenimiento preventivo.
                        </div>
                    """, unsafe_allow_html=True)
                elif tendencia_reciente[1] < tendencia_reciente[0]:
                    diferencia = tendencia_reciente[0] - tendencia_reciente[1]
                    porcentaje = (diferencia / tendencia_reciente[0]) * 100
                    st.markdown(f"""
                        <div class="alert-success">
                            <strong>📉 Tendencia a la Baja:</strong> Las fallas disminuyeron {diferencia} casos ({porcentaje:.1f}%) 
                            respecto al mes anterior. ¡Excelente trabajo!
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="alert-info">
                    <strong>ℹ️ Sin datos temporales:</strong> No hay suficientes datos de fallas con fechas para mostrar tendencias.
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-dashboard"></div>', unsafe_allow_html=True)
    
    # RESUMEN EJECUTIVO (SOLO ADMIN)
    if es_admin:
        st.markdown("""
            <div class="section-header">
                <h3>📋 Resumen Ejecutivo</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="help-main">
                <h3>🎯 Estado General del Sistema</h3>
                <p>Basado en los datos actuales, aquí está el resumen de tu operación:</p>
            </div>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown(f"""
                <div class="chart-container">
                    <h4>📊 Indicadores Clave</h4>
                    <p><span class="stats-badge">👥 {total_usuarios} Usuarios</span></p>
                    <p><span class="stats-badge">🔧 {total_fallas} Fallas Total</span></p>
                    <p><span class="stats-badge">📦 {total_materiales} Materiales</span></p>
                    <p><span class="stats-badge">📅 {fallas_este_mes} Fallas/Mes</span></p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_res2:
            st.markdown("""
                <div class="chart-container">
                    <h4>💡 Recomendaciones</h4>
                    <ul style="margin: 0.5rem 0;">
                        <li>Revisa diariamente el dashboard para detectar anomalías</li>
                        <li>Mantén el inventario actualizado</li>
                        <li>Programa mantenimientos preventivos</li>
                        <li>Capacita al equipo en reporte de fallas</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    else:
        # Resumen simple para empleados
        st.markdown("""
            <div class="section-header">
                <h3>📋 Resumen de Fallas</h3>
            </div>
        """, unsafe_allow_html=True)
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown(f"""
                <div class="chart-container">
                    <h4>📊 Tus Métricas</h4>
                    <p><span class="stats-badge">🔧 {total_fallas} Fallas Total</span></p>
                    <p><span class="stats-badge">📅 {fallas_este_mes} Este Mes</span></p>
                    <p><span class="stats-badge">🎯 Enfoque en Prevención</span></p>
                </div>
            """, unsafe_allow_html=True)
        
        with col_res2:
            st.markdown("""
                <div class="chart-container">
                    <h4>💡 Para Empleados</h4>
                    <ul style="margin: 0.5rem 0;">
                        <li>Reporta fallas inmediatamente</li>
                        <li>Revisa los lugares críticos</li>
                        <li>Sigue los protocolos de seguridad</li>
                        <li>Comunica anomalías al supervisor</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)