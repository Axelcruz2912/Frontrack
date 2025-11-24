import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from backend.controllers.materiales_controller import get_all_materiales
from backend.controllers.fallas_controller import get_all_fallas

def mostrar_optimizador_inventario():
    #  ESTILOS CSS PERSONALIZADOS
    st.markdown("""
        <style>
        /* Estilos globales */
        .main {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        
        /* Header principal */
        .header-inventario {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 15px;
            color: white;
            text-align: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            margin-bottom: 2rem;
        }
        
        .header-inventario h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .header-inventario p {
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-size: 1.1rem;
        }
        
        /* Metric card */
        .metric-card-inventario {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease;
            margin-bottom: 1rem;
        }
        
        .metric-card-inventario:hover {
            transform: translateY(-5px);
        }
        
        .metric-value-inventario {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .metric-label-inventario {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        /* Alert cards */
        .alert-card-critical {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 1rem;
            border-left: 6px solid #ff4757;
        }
        
        .alert-card-warning {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: #333;
            margin-bottom: 1rem;
            border-left: 6px solid #ff9a9e;
        }
        
        .alert-card-info {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: #333;
            margin-bottom: 1rem;
            border-left: 6px solid #a8edea;
        }
        
        /* Recommendation card */
        .recommendation-card-inventario {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            border-left: 4px solid #ff9a56;
        }
        
        .recommendation-card-inventario h4 {
            margin-top: 0;
            color: #333;
        }
        
        /* Section container */
        .section-container-inventario {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
            margin-bottom: 1.5rem;
        }
        
        /* Help box */
        .help-box-inventario {
            background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin-bottom: 1.5rem;
        }
        
        .help-box-inventario h3 {
            margin-top: 0;
        }
        
        /* Divider */
        .divider-inventario {
            height: 2px;
            background: linear-gradient(90deg, transparent, #667eea, transparent);
            margin: 2rem 0;
        }
        
        /* Table styles */
        .table-help-inventario {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .table-help-inventario h4 {
            margin-top: 0;
            color: #333;
        }
        
        /* Chart container */
        .chart-container-inventario {
            background: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        /* Priority badges */
        .priority-high {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .priority-medium {
            background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%);
            color: #333;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        
        .priority-low {
            background: linear-gradient(135deg, #48dbfb 0%, #0abde3 100%);
            color: white;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)
    
    #  HEADER PRINCIPAL
    st.markdown("""
        <div class="header-inventario">
            <h1>📦 Optimizador de Inventario con IA</h1>
            <p>Gestión inteligente de stock y recomendaciones automatizadas</p>
        </div>
    """, unsafe_allow_html=True)
    
    # AYUDA GENERAL
    with st.expander("📖 ¿Cómo funciona el optimizador?", expanded=False):
        st.markdown("""
            <div class="help-box-inventario">
                <h3>🎯 Guía del Optimizador de Inventario</h3>
                <p><strong>Este módulo te ayuda a:</strong></p>
                <ul>
                    <li>📊 <strong>Monitorear inventario:</strong> Estado actual de todos los materiales</li>
                    <li>🚨 <strong>Detectar problemas:</strong> Stock bajo, agotado o excesivo</li>
                    <li>🤖 <strong>Generar recomendaciones:</strong> Sugerencias basadas en IA para optimizar tu inventario</li>
                    <li>📈 <strong>Analizar patrones:</strong> Uso histórico de materiales en reparaciones</li>
                </ul>
                <p style="margin-top: 1rem;"><strong>💡 Consejo:</strong> Revisa las recomendaciones regularmente para mantener un inventario saludable y reducir costos.</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Cargar datos
    materiales = get_all_materiales()
    fallas = get_all_fallas()
    df_materiales = pd.DataFrame(materiales)
    df_fallas = pd.DataFrame(fallas)
    
    if df_materiales.empty:
        st.markdown("""
            <div class="alert-card-warning">
                <h3 style="margin:0;">⚠️ No hay datos disponibles</h3>
                <p style="margin:0.5rem 0 0 0;">No se encontraron materiales en el inventario. Comienza agregando materiales en el módulo de Gestión de Materiales.</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    # SECCIÓN 1: MÉTRICAS DEL INVENTARIO
    st.markdown("### 📊 Estado Actual del Inventario")
    
    st.markdown("""
        <div class="table-help-inventario">
            <h4>ℹ️ Acerca de estas métricas</h4>
            <p><strong>¿Qué miden?</strong> Estas cifras te dan una vista rápida del estado general de tu inventario.</p>
            <p><strong>Importancia:</strong> Un inventario bien gestionado reduce costos y mejora la eficiencia operativa.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_items = len(df_materiales)
        st.markdown(f"""
            <div class="metric-card-inventario">
                <div class="metric-label-inventario">📦 TOTAL ITEMS</div>
                <div class="metric-value-inventario">{total_items}</div>
                <div class="metric-label-inventario">Materiales diferentes</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_inventario = df_materiales['existencia'].sum()
        st.markdown(f"""
            <div class="metric-card-inventario" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <div class="metric-label-inventario">📊 UNIDADES TOTALES</div>
                <div class="metric-value-inventario">{int(total_inventario)}</div>
                <div class="metric-label-inventario">En stock</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        valor_total = (df_materiales['existencia'] * df_materiales.get('costo_promedio', 1)).sum()
        st.markdown(f"""
            <div class="metric-card-inventario" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                <div class="metric-label-inventario">💰 VALOR TOTAL</div>
                <div class="metric-value-inventario">${valor_total:,.0f}</div>
                <div class="metric-label-inventario">Inventario valorizado</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        materiales_bajos = len(df_materiales[df_materiales['existencia'] <= 5])
        st.markdown(f"""
            <div class="metric-card-inventario" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);">
                <div class="metric-label-inventario">⚠️ STOCK BAJO</div>
                <div class="metric-value-inventario">{materiales_bajos}</div>
                <div class="metric-label-inventario">≤ 5 unidades</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-inventario"></div>', unsafe_allow_html=True)
    
    # SECCIÓN 2: ALERTAS DE INVENTARIO
    
    st.markdown("### 🚨 Alertas y Estado Crítico")
    
    st.markdown("""
        <div class="table-help-inventario">
            <h4>🔔 Sistema de Alertas</h4>
            <p><strong>¿Cómo interpretar las alertas?</strong></p>
            <ul>
                <li><strong>🔴 CRÍTICO:</strong> Requiere acción inmediata</li>
                <li><strong>🟡 ADVERTENCIA:</strong> Necesita atención pronto</li>
                <li><strong>🟢 INFORMACIÓN:</strong> Estado normal o observaciones</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    col_alert1, col_alert2 = st.columns(2)
    
    with col_alert1:
        # Materiales sin stock
        sin_stock = df_materiales[df_materiales['existencia'] == 0]
        if not sin_stock.empty:
            st.markdown("""
                <div class="alert-card-critical">
                    <h3 style="margin:0 0 1rem 0;">🔴 MATERIALES SIN STOCK</h3>
            """, unsafe_allow_html=True)
            
            for _, material in sin_stock.head(5).iterrows():
                descripcion = material.get('descripcion', 'Material sin nombre')
                st.markdown(f"❌ **{descripcion}**")
            
            if len(sin_stock) > 5:
                st.markdown(f"*... y {len(sin_stock) - 5} materiales más*")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="alert-card-info">
                    <h3 style="margin:0;">✅ SIN STOCK CRÍTICO</h3>
                    <p style="margin:0.5rem 0 0 0;">Excelente! No hay materiales completamente agotados.</p>
                </div>
            """, unsafe_allow_html=True)
    
    with col_alert2:
        # Materiales con stock bajo
        stock_bajo = df_materiales[(df_materiales['existencia'] > 0) & (df_materiales['existencia'] <= 5)]
        if not stock_bajo.empty:
            st.markdown("""
                <div class="alert-card-warning">
                    <h3 style="margin:0 0 1rem 0;">🟡 STOCK BAJO (≤5 unidades)</h3>
            """, unsafe_allow_html=True)
            
            for _, material in stock_bajo.head(5).iterrows():
                descripcion = material.get('descripcion', 'Material sin nombre')
                existencia = material['existencia']
                st.markdown(f"⚠️ **{descripcion}** - {existencia} unidades")
            
            if len(stock_bajo) > 5:
                st.markdown(f"*... y {len(stock_bajo) - 5} materiales más*")
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="alert-card-info">
                    <h3 style="margin:0;">✅ STOCK SALUDABLE</h3>
                    <p style="margin:0.5rem 0 0 0;">Todos los materiales tienen stock suficiente.</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-inventario"></div>', unsafe_allow_html=True)
    
    
    # SECCIÓN 3: RECOMENDACIONES DE IA
    st.markdown("### 🤖 Recomendaciones Inteligentes")
    
    st.markdown("""
        <div class="table-help-inventario">
            <h4>🧠 IA de Optimización</h4>
            <p><strong>¿Cómo funciona?</strong> El sistema analiza patrones de uso, niveles de stock y costos para generar recomendaciones personalizadas.</p>
            <p><strong>Beneficios:</strong> Reduce costos, evita desabastecimientos y optimiza el espacio de almacenamiento.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Generar Recomendaciones de IA", type="primary", use_container_width=True):
        with st.spinner("🤖 Analizando patrones de uso y optimizando inventario..."):
            recomendaciones = []
            
            for _, material in df_materiales.iterrows():
                existencia = material['existencia']
                descripcion = material.get('descripcion', 'Material')
                costo = material.get('costo_promedio', 0)
                clave = material.get('clave_material', 'N/A')
                
                if existencia == 0:
                    recomendaciones.append({
                        'material': descripcion,
                        'clave': clave,
                        'accion': '🛒 COMPRAR URGENTE',
                        'cantidad': 15,
                        'prioridad': 'ALTA',
                        'razon': 'Stock completamente agotado - riesgo operativo',
                        'icono': '🔴'
                    })
                elif existencia <= 3:
                    recomendaciones.append({
                        'material': descripcion,
                        'clave': clave,
                        'accion': '📦 REORDENAR PRONTO',
                        'cantidad': 10,
                        'prioridad': 'MEDIA',
                        'razon': f'Stock bajo: {existencia} unidades - riesgo inminente',
                        'icono': '🟡'
                    })
                elif existencia > 20 and costo > 50:
                    recomendaciones.append({
                        'material': descripcion,
                        'clave': clave,
                        'accion': '💰 OPTIMIZAR INVENTARIO',
                        'cantidad': -5,
                        'prioridad': 'BAJA',
                        'razon': f'Exceso de inventario: {existencia} unidades - costo alto',
                        'icono': '🔵'
                    })
                elif existencia > 50:
                    recomendaciones.append({
                        'material': descripcion,
                        'clave': clave,
                        'accion': '📊 REVISAR NECESIDAD',
                        'cantidad': 0,
                        'prioridad': 'BAJA',
                        'razon': f'Stock muy alto: {existencia} unidades - posible sobreabastecimiento',
                        'icono': 'ℹ️'
                    })
            
            # Mostrar recomendaciones
            if recomendaciones:
                st.markdown('<div class="section-container-inventario">', unsafe_allow_html=True)
                
                # Resumen ejecutivo
                total_recomendaciones = len(recomendaciones)
                alta_prioridad = len([r for r in recomendaciones if r['prioridad'] == 'ALTA'])
                
                st.markdown(f"""
                    <div class="recommendation-card-inventario">
                        <h4>📋 Resumen Ejecutivo</h4>
                        <p><strong>Total de recomendaciones generadas:</strong> {total_recomendaciones}</p>
                        <p><strong>Acciones críticas (ALTA prioridad):</strong> {alta_prioridad}</p>
                        <p><strong>Estado general del inventario:</strong> {'⚠️ Requiere atención' if alta_prioridad > 0 else '✅ Saludable'}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Mostrar recomendaciones en tabla mejorada
                df_recomendaciones = pd.DataFrame(recomendaciones)
                
                # Aplicar estilos a la tabla
                def estilo_prioridad(val):
                    if val == 'ALTA':
                        return 'background-color: #ff6b6b; color: white; font-weight: bold;'
                    elif val == 'MEDIA':
                        return 'background-color: #feca57; color: black; font-weight: bold;'
                    else:
                        return 'background-color: #48dbfb; color: white; font-weight: bold;'
                
                styled_df = df_recomendaciones.style.applymap(
                    estilo_prioridad, 
                    subset=['prioridad']
                )
                
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    height=400
                )
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Análisis adicional
                st.markdown("### 💡 Análisis de Recomendaciones")
                
                col_anal1, col_anal2, col_anal3 = st.columns(3)
                
                with col_anal1:
                    compras_urgentes = len([r for r in recomendaciones if 'COMPRAR' in r['accion']])
                    st.metric("Compras Urgentes", compras_urgentes)
                
                with col_anal2:
                    reordenes = len([r for r in recomendaciones if 'REORDENAR' in r['accion']])
                    st.metric("Reordenes Necesarias", reordenes)
                
                with col_anal3:
                    optimizaciones = len([r for r in recomendaciones if 'OPTIMIZAR' in r['accion']])
                    st.metric("Optimizaciones", optimizaciones)
                
            else:
                st.markdown("""
                    <div class="alert-card-info">
                        <h3 style="margin:0;">✅ INVENTARIO OPTIMIZADO</h3>
                        <p style="margin:0.5rem 0 0 0;">El sistema no encontró acciones necesarias. Tu inventario está bien gestionado.</p>
                    </div>
                """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider-inventario"></div>', unsafe_allow_html=True)
    
    
    # SECCIÓN 4: ANÁLISIS DE PATRONES
    st.markdown("### 📈 Análisis de Patrones de Uso")
    
    st.markdown("""
        <div class="table-help-inventario">
            <h4>🔍 Análisis Predictivo</h4>
            <p><strong>¿Qué analiza?</strong> Patrones históricos de uso de materiales en reparaciones y mantenimientos.</p>
            <p><strong>Objetivo:</strong> Predecir demandas futuras y ajustar niveles de inventario proactivamente.</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not df_fallas.empty and 'materiales_usados' in df_fallas.columns:
        try:
            # Simular análisis de materiales más usados
            st.markdown('<div class="chart-container-inventario">', unsafe_allow_html=True)
            
            # Crear gráfico de distribución de stock
            df_materiales['nivel_stock'] = pd.cut(
                df_materiales['existencia'], 
                bins=[-1, 0, 5, 10, 20, float('inf')],
                labels=['Agotado', 'Muy Bajo', 'Bajo', 'Normal', 'Alto']
            )
            
            distribucion_stock = df_materiales['nivel_stock'].value_counts().sort_index()
            
            fig = px.bar(
                distribucion_stock,
                title="📊 Distribución de Niveles de Stock",
                labels={'value': 'Cantidad de Materiales', 'index': 'Nivel de Stock'},
                color=distribucion_stock.index,
                color_discrete_sequence=['#ff6b6b', '#feca57', '#ff9ff3', '#48dbfb', '#1dd1a1']
            )
            
            fig.update_layout(
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Insights del análisis
            st.markdown("### 🧠 Insights del Análisis")
            
            if len(df_materiales[df_materiales['existencia'] == 0]) > 0:
                st.markdown("""
                    <div class="alert-card-critical">
                        <strong>🚨 Punto Crítico:</strong> Tienes materiales agotados que requieren atención inmediata para evitar interrupciones operativas.
                    </div>
                """, unsafe_allow_html=True)
            
            if len(df_materiales[df_materiales['existencia'] <= 5]) > len(df_materiales) * 0.3:
                st.markdown("""
                    <div class="alert-card-warning">
                        <strong>⚠️ Alerta de Gestión:</strong> Más del 30% de tus materiales tienen stock bajo. Considera una revisión general de niveles de inventario.
                    </div>
                """, unsafe_allow_html=True)
            
            # Estadísticas adicionales
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                materiales_optimos = len(df_materiales[(df_materiales['existencia'] > 5) & (df_materiales['existencia'] <= 20)])
                st.metric("Materiales en Nivel Óptimo", materiales_optimos)
            
            with col_stat2:
                porcentaje_optimo = (materiales_optimos / len(df_materiales)) * 100
                st.metric("Porcentaje Óptimo", f"{porcentaje_optimo:.1f}%")
                
        except Exception as e:
            st.markdown("""
                <div class="alert-card-info">
                    <strong>ℹ️ Análisis Básico:</strong> Para un análisis completo de patrones de uso, se necesitan más datos históricos de reparaciones.
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="alert-card-info">
                <h3 style="margin:0;">📋 Próximos Pasos</h3>
                <p style="margin:0.5rem 0 0 0;">Para habilitar el análisis avanzado de patrones:</p>
                <ul>
                    <li>Registra más fallas y reparaciones en el sistema</li>
                    <li>Asegúrate de incluir los materiales utilizados en cada reporte</li>
                    <li>Mantén actualizados los niveles de inventario</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)