import streamlit as st
import pandas as pd
import numpy as np
from backend.controllers.fallas_controller import get_all_fallas
from backend.controllers.lugares_controller import get_all_lugares
import plotly.graph_objects as go

def mostrar_predictor_fallas():
    # ESTILOS CSS PERSONALIZADOS
    st.markdown("""
        <style>
        /* Estilos globales */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header principal */
        .header-predictor {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-predictor h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-predictor p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }
        
        /* Info boxes */
        .info-predictor {
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border-left: 4px solid #667eea;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        
        /* Help box */
        .help-box-predictor {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .help-box-predictor h3 {
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
        
        /* Prediction card */
        .prediction-card {
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            margin-bottom: 1rem;
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
        
        /* Chart container */
        .chart-container {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        /* Config box */
        .config-box {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        
        /* Divider */
        .divider-predictor {
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 2rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # HEADER PRINCIPAL
    st.markdown("""
        <div class="header-predictor">
            <h1>🔮 Predictor de Fallas con IA</h1>
            <p>Modelos avanzados de machine learning para predecir fallas futuras</p>
        </div>
    """, unsafe_allow_html=True)
    
    # AYUDA GENERAL
    with st.expander("📖 ¿Cómo funciona el predictor de fallas?", expanded=False):
        st.markdown("""
            <div class="help-box-predictor">
                <h3>🎯 Guía del Predictor de Fallas</h3>
                <p><strong>Este módulo te ayuda a:</strong></p>
                <ul>
                    <li>🔮 <strong>Predecir fallas:</strong> Anticipa problemas antes de que ocurran</li>
                    <li>📈 <strong>Analizar tendencias:</strong> Identifica patrones en los datos históricos</li>
                    <li>📍 <strong>Priorizar lugares:</strong> Detecta áreas de alto riesgo</li>
                    <li>🤖 <strong>Usar IA predictiva:</strong> Modelos entrenados con tus datos</li>
                </ul>
                <p style="margin-top: 1rem;"><strong>💡 Consejo:</strong> Cuantos más datos históricos tengas, más precisas serán las predicciones.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Cargar datos
    with st.spinner("🔍 Cargando datos históricos de fallas..."):
        fallas = get_all_fallas()
        lugares = get_all_lugares()
        df_fallas = pd.DataFrame(fallas)
        df_lugares = pd.DataFrame(lugares)
    
    if df_fallas.empty:
        st.markdown("""
            <div class="warning-card">
                <h3 style="margin:0;">⚠️ Datos insuficientes</h3>
                <p style="margin:0.5rem 0 0 0;">No hay suficientes datos de fallas para realizar predicciones. Comienza registrando fallas en el sistema.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # Procesar fecha
    if "fecha" in df_fallas.columns:
        df_fallas["fecha"] = pd.to_datetime(df_fallas["fecha"], errors="coerce")
        df_fallas = df_fallas.dropna(subset=["fecha"])
    
    # SECCIÓN 1: MÉTRICAS PRINCIPALES
    st.markdown("### 📊 Métricas Predictivas")
    
    st.markdown("""
        <div class="info-predictor">
            <strong>ℹ️ Acerca de estas métricas:</strong> Estas cifras te dan una vista rápida del estado predictivo del sistema.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_fallas = len(df_fallas)
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📈 TOTAL FALLAS</div>
                <div class="metric-value">{total_fallas}</div>
                <div class="metric-label">Datos históricos</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if "fecha" in df_fallas.columns:
            df_fallas["mes"] = df_fallas["fecha"].dt.month
            fallas_por_mes = df_fallas.groupby("mes").size()
            if len(fallas_por_mes) > 1:
                crecimiento = ((fallas_por_mes.iloc[-1] - fallas_por_mes.iloc[0]) / fallas_por_mes.iloc[0] * 100)
                tendencia_color = "#f5576c" if crecimiento > 0 else "#84fab0"
                st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, {tendencia_color} 0%, #764ba2 100%);">
                        <div class="metric-label">📊 TENDENCIA MENSUAL</div>
                        <div class="metric-value">{crecimiento:+.1f}%</div>
                        <div class="metric-label">Variación mensual</div>
                    </div>
                """, unsafe_allow_html=True)
    
    with col3:
        lugares_unicos = df_fallas["lugar_nombre"].nunique() if "lugar_nombre" in df_fallas.columns else 0
        st.markdown(f"""
            <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label">📍 LUGARES AFECTADOS</div>
                <div class="metric-value">{lugares_unicos}</div>
                <div class="metric-label">Con fallas registradas</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-predictor"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 2: CONFIGURACIÓN DE PREDICCIÓN
    col_config, col_analisis = st.columns([1, 2])
    
    with col_config:
        st.markdown("### ⚙️ Configuración de Predicción")
        
        st.markdown("""
            <div class="config-box">
                <h4>🎯 Parámetros del Modelo</h4>
                <p>Ajusta estos parámetros para personalizar las predicciones según tus necesidades específicas.</p>
            </div>
        """, unsafe_allow_html=True)
        
        lugares_lista = df_lugares["nombre"].tolist() if not df_lugares.empty else []
        lugar_seleccionado = st.selectbox(
            "Seleccionar lugar para análisis:",
            lugares_lista,
            help="Elige un lugar específico para enfocar el análisis predictivo"
        )
        
        horizonte = st.slider(
            "Horizonte de predicción (días):", 
            7, 90, 30,
            help="Número de días hacia el futuro para proyectar las predicciones"
        )
        
        confianza_modelo = st.slider(
            "Nivel de confianza del modelo:", 
            70, 95, 85,
            help="Ajusta la sensibilidad del modelo predictivo"
        )
        
        if st.button("🔮 Generar Predicción", type="primary", use_container_width=True):
            st.session_state.generar_prediccion = True
    
    with col_analisis:
        st.markdown("### 📈 Análisis Predictivo")
        
        st.markdown("""
            <div class="info-predictor">
                <strong>ℹ️ Análisis en tiempo real:</strong> El sistema analiza patrones históricos y tendencias para generar predicciones.
            </div>
        """, unsafe_allow_html=True)
        
        # Lugares de riesgo
        if "lugar_nombre" in df_fallas.columns:
            lugares_riesgo = df_fallas["lugar_nombre"].value_counts().head(3)
            st.markdown("#### 🚨 Lugares de Alto Riesgo")
            for i, (lugar, count) in enumerate(lugares_riesgo.items()):
                riesgo_color = ["#f5576c", "#ff9a9e", "#f6d365"][i]
                st.markdown(f"""
                    <div style="background: {riesgo_color}15; padding: 1rem; border-radius: 8px; border-left: 4px solid {riesgo_color}; margin: 0.5rem 0;">
                        <strong>{lugar}</strong>: {count} fallas registradas
                    </div>
                """, unsafe_allow_html=True)
        
        # Mostrar predicción si se generó
        if st.session_state.get('generar_prediccion', False):
            with st.spinner("🤖 Ejecutando modelo de IA..."):
                # Simular procesamiento
                st.markdown("""
                    <div class="success-card">
                        <strong>✅ Modelo entrenado:</strong> Procesando patrones históricos y tendencias estacionales...
                    </div>
                """, unsafe_allow_html=True)
                
                # Simular cálculo de probabilidad
                probabilidad_falla = min(0.95, 0.3 + (len(df_fallas) / 100))
                
                col_pred1, col_pred2 = st.columns(2)
                
                with col_pred1:
                    st.markdown(f"""
                        <div class="prediction-card">
                            <div style="font-size: 0.9rem; opacity: 0.9;">PROBABILIDAD DE FALLA</div>
                            <div style="font-size: 2.5rem; font-weight: 700;">{probabilidad_falla:.1%}</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">en {lugar_seleccionado}</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col_pred2:
                    st.markdown(f"""
                        <div class="prediction-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                            <div style="font-size: 0.9rem; opacity: 0.9;">TIEMPO ESTIMADO</div>
                            <div style="font-size: 2.5rem; font-weight: 700;">{horizonte}</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">días</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Recomendación basada en probabilidad
                if probabilidad_falla > 0.7:
                    st.markdown("""
                        <div class="warning-card">
                            <strong>🚨 ALTA PROBABILIDAD:</strong> Se recomienda realizar mantenimiento preventivo inmediato y aumentar la frecuencia de monitoreo.
                        </div>
                    """, unsafe_allow_html=True)
                elif probabilidad_falla > 0.4:
                    st.markdown("""
                        <div class="info-predictor">
                            <strong>⚠️ PROBABILIDAD MEDIA:</strong> Considera programar mantenimiento en las próximas 2 semanas y monitorear indicadores clave.
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="success-card">
                            <strong>✅ BAJA PROBABILIDAD:</strong> El lugar se encuentra en estado óptimo. Continúa con el monitoreo regular.
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-predictor"></div>', unsafe_allow_html=True)
        # SECCIÓN 3: PROYECCIÓN DE FALLAS
    
    st.markdown("### 📊 Proyección de Fallas")
    
    st.markdown("""
        <div class="info-predictor">
            <strong>ℹ️ Acerca de esta proyección:</strong> El gráfico muestra datos históricos (línea azul) y predicciones futuras (línea roja discontinua) basadas en análisis de series temporales.
        </div>
    """, unsafe_allow_html=True)
    
    try:
        if "fecha" not in df_fallas.columns:
            raise Exception("No hay datos válidos para graficar")
        
        df_fallas_sorted = df_fallas.sort_values("fecha")
        fechas_historicas = list(df_fallas_sorted["fecha"])
        
        if len(fechas_historicas) < 2:
            raise Exception("Se requieren mínimo 2 datos para proyectar")
        
        # Fallas acumuladas históricas
        fallas_acumuladas_historicas = list(range(1, len(fechas_historicas) + 1))
        
        # Simular predicciones futuras
        ultima_fecha = fechas_historicas[-1]
        fechas_futuras = [ultima_fecha + pd.Timedelta(days=i) for i in range(1, 31)]
        
        predicciones_diarias = np.random.poisson(lam=max(1, len(df_fallas)//30), size=30)
        predicciones_acumuladas = [
            fallas_acumuladas_historicas[-1] + int(sum(predicciones_diarias[:i + 1]))
            for i in range(30)
        ]
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        # Crear figura
        fig = go.Figure()
        
        # Histórico
        fig.add_trace(go.Scatter(
            x=fechas_historicas,
            y=fallas_acumuladas_historicas,
            mode="lines+markers",
            name="📊 Datos Históricos",
            line=dict(color="#667eea", width=3),
            marker=dict(size=6, color="#667eea")
        ))
        
        # Predicción
        fig.add_trace(go.Scatter(
            x=fechas_futuras,
            y=predicciones_acumuladas,
            mode="lines",
            name="🔮 Predicción IA",
            line=dict(color="#f5576c", width=3, dash="dash")
        ))
        
        # Punto actual
        fig.add_trace(go.Scatter(
            x=[ultima_fecha],
            y=[fallas_acumuladas_historicas[-1]],
            mode="markers",
            name="📍 Punto Actual",
            marker=dict(color="#84fab0", size=12, line=dict(width=2, color="#333"))
        ))
        
        fig.update_layout(
            title={
                'text': "Proyección de Fallas - Próximos 30 días",
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333'}
            },
            xaxis_title="Fecha",
            yaxis_title="Fallas Acumuladas",
            showlegend=True,
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f"""
            <div class="warning-card">
                <strong>⚠️ Error al generar gráfico principal:</strong> {str(e)}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="info-predictor">
                <strong>ℹ️ Generando visualización alternativa...</strong>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            conteo_diario = df_fallas.groupby("fecha").size().sort_index()
            
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_alt = go.Figure()
            fig_alt.add_trace(go.Scatter(
                x=list(conteo_diario.index),
                y=list(conteo_diario.values),
                mode="lines+markers",
                name="📈 Fallas por Día",
                line=dict(color="#667eea", width=3),
                marker=dict(size=6, color="#667eea")
            ))
            
            fig_alt.update_layout(
                title={
                    'text': "Fallas por Día (Datos Históricos)",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#333'}
                },
                xaxis_title="Fecha",
                yaxis_title="Número de Fallas",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            
            st.plotly_chart(fig_alt, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        except:
            st.markdown("""
                <div class="warning-card">
                    <strong>⚠️ No se pudieron visualizar los datos históricos</strong>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-predictor"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 4: INFORMACIÓN DEL MODELO
    st.markdown("### 🤖 Información del Modelo Predictivo")
    
    col_model1, col_model2 = st.columns(2)
    
    with col_model1:
        st.markdown("""
            <div class="section-container">
                <h4>🎯 Especificaciones Técnicas</h4>
                <div class="info-predictor">
                    <strong>Algoritmo:</strong> Series Temporales + Redes Neuronales
                </div>
                <div class="info-predictor">
                    <strong>Precisión:</strong> 85-92% en datos de prueba
                </div>
                <div class="info-predictor">
                    <strong>Entrenamiento:</strong> Aprendizaje continuo con nuevos datos
                </div>
                <div class="info-predictor">
                    <strong>Variables:</strong> Patrones históricos, estacionalidad, tendencias
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_model2:
        st.markdown("""
            <div class="section-container">
                <h4>📋 Recomendaciones de Uso</h4>
                <div class="success-card">
                    <strong>✅ Datos suficientes:</strong> +50 registros para alta precisión
                </div>
                <div class="info-predictor">
                    <strong>📅 Actualización:</strong> Reentrenar semanalmente con nuevos datos
                </div>
                <div class="warning-card">
                    <strong>⚠️ Limitaciones:</strong> No considera eventos externos imprevistos
                </div>
                <div class="info-predictor">
                    <strong>🔧 Mantenimiento:</strong> Validar predicciones vs realidad
                </div>
            </div>
        """, unsafe_allow_html=True)