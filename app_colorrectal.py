import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ==========================================
st.set_page_config(
    page_title="OncoTwin - Gemelo Digital Oncológico Integrativo",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ENCABEZADO Y DESCRIPCIÓN
# ==========================================
st.markdown('<p class="main-header">🧬 OncoTwin: Gemelo Digital Oncológico Integrativo</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Plataforma de simulación biomecánica, validación cruzada y evaluación de sinergia tri-pilar adaptada a la epidemiología chilena.</p>', unsafe_allow_html=True)
st.divider()

# ==========================================
# 3. BARRA LATERAL: PERFILAMIENTO CLÍNICO
# ==========================================
st.sidebar.header("📋 Panel de Perfilamiento Clínico")

# 10 Cánceres más prevalentes en Chile (MINSAL / GLOBOCAN)
CANCERES_CHILE = [
    "Cáncer de Próstata",
    "Cáncer de Mama",
    "Cáncer Colorrectal",
    "Cáncer Gástrico (Estómago)",
    "Cáncer de Pulmón",
    "Cáncer de Vesícula Biliar",
    "Cáncer Cervicouterino",
    "Cáncer de Riñón",
    "Cáncer de Ovarios",
    "Cáncer Tiroideo / Melanoma Cutáneo"
]

nombre_paciente = st.sidebar.text_input("Identificador del Paciente", value="Paciente Ref-2026-CH")
edad_paciente = st.sidebar.number_input("Edad (años)", min_value=18, max_value=110, value=58)
genero_paciente = st.sidebar.selectbox("Género Biológico", ["Femenino", "Masculino"])

diagnostico_cancer = st.sidebar.selectbox(
    "Diagnóstico Oncológico Principal (Epidemiología Chile)",
    options=CANCERES_CHILE,
    index=2  # Colorrectal por defecto
)

estadio_clinico = st.sidebar.selectbox(
    "Estadio Clínico (TNM / FIGO)",
    ["Estadio I", "Estadio II", "Estadio III", "Estadio IV (Metastásico)"]
)

st.sidebar.divider()
st.sidebar.header("⚙️ Parámetros Biológicos del Tumor")

volumen_inicial = st.sidebar.slider(
    "Volumen Tumoral Inicial (V₀ cm³)",
    min_value=1.0, max_value=100.0, value=25.0, step=0.5
)

capacidad_carga = st.sidebar.slider(
    "Capacidad de Carga Espacial (K cm³)",
    min_value=50.0, max_value=500.0, value=200.0, step=10.0
)

tasa_crecimiento = st.sidebar.slider(
    "Tasa de Crecimiento Intrínseco (r)",
    min_value=0.01, max_value=0.20, value=0.05, step=0.005
)

dias_simulacion = st.sidebar.slider(
    "Horizonte de Simulación (Días)",
    min_value=30, max_value=365, value=120, step=10
)

# ==========================================
# 4. TABLA INTERACTIVA: LOS 3 PILARES
# ==========================================
st.subheader("💊 Esquema Terapéutico Multi-Pilar (Grilla Interactiva)")
st.caption("Edite, agregue o clasifique las intervenciones ingresando su dosificación y eficacia estimada.")

# Datos por defecto que representan los 3 pilares activos
datos_iniciales = pd.DataFrame([
    {
        "Compuesto / Tratamiento": "Oxaliplatino / Capecitabina",
        "Pilar": "Soporte Químico",
        "Dosis Diaria (mg)": 85.0,
        "Eficacia Teórica (0.0 - 1.0)": 0.45,
        "Estado": True
    },
    {
        "Compuesto / Tratamiento": "Extracto Botánico Bioactivo (Curcumina/EGCG)",
        "Pilar": "Apoyo Natural",
        "Dosis Diaria (mg)": 500.0,
        "Eficacia Teórica (0.0 - 1.0)": 0.20,
        "Estado": True
    },
    {
        "Compuesto / Tratamiento": "Factor Regenerativo / Inmunomodulador",
        "Pilar": "Terapia Regenerativa",
        "Dosis Diaria (mg)": 100.0,
        "Eficacia Teórica (0.0 - 1.0)": 0.30,
        "Estado": True
    }
])

# Configuración de columnas interactivas para Streamlit
config_columnas = {
    "Compuesto / Tratamiento": st.column_config.TextColumn("Compuesto / Tratamiento", required=True, width="medium"),
    "Pilar": st.column_config.SelectboxColumn(
        "Pilar Terapéutico",
        options=["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"],
        required=True,
        width="medium"
    ),
    "Dosis Diaria (mg)": st.column_config.NumberColumn("Dosis Diaria (mg)", min_value=0.0, max_value=5000.0, step=5.0, format="%.1f mg"),
    "Eficacia Teórica (0.0 - 1.0)": st.column_config.NumberColumn("Eficacia (0.0 a 1.0)", min_value=0.0, max_value=1.0, step=0.05, format="%.2f"),
    "Estado": st.column_config.CheckboxColumn("Activo en Simulación", default=True)
}

# Grilla interactiva reactiva
df_grilla = st.data_editor(
    datos_iniciales,
    column_config=config_columnas,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_pilares"
)

# Sanitización estricta de datos (previene corrupciones de tipos o nulos)
df_grilla["Dosis Diaria (mg)"] = pd.to_numeric(df_grilla["Dosis Diaria (mg)"]).fillna(0.0)
df_grilla["Eficacia Teórica (0.0 - 1.0)"] = pd.to_numeric(df_grilla["Eficacia Teórica (0.0 - 1.0)"]).fillna(0.0)
df_grilla["Estado"] = df_grilla["Estado"].astype(bool)

# Filtrar solo compuestos activos
df_activos = df_grilla[df_grilla["Estado"] == True]

# ==========================================
# 5. MOTOR DE VALIDACIÓN CRUZADA BIOLÓGICA
# ==========================================
st.divider()
st.subheader("🛡️ Motor de Validación Cruzada y Auditoría Terapéutica")

# Análisis dinámico del esquema ingresado
tiene_quimico = any((df_activos["Pilar"] == "Soporte Químico") & (df_activos["Eficacia Teórica (0.0 - 1.0)"] > 0))
tiene_natural = any((df_activos["Pilar"] == "Apoyo Natural") & (df_activos["Eficacia Teórica (0.0 - 1.0)"] > 0))
tiene_regenerativo = any((df_activos["Pilar"] == "Terapia Regenerativa") & (df_activos["Eficacia Teórica (0.0 - 1.0)"] > 0))

# Evaluación de Sinergia Biológica
aplica_sinergia = tiene_quimico and tiene_natural
factor_sinergia = 1.25 if aplica_sinergia else 1.00  # +25% de bonus por sinergia integrativa

# Alertas dinámicas de seguridad y consistencia
col_val1, col_val2 = st.columns(2)

with col_val1:
    st.markdown("##### 🔍 Auditoría de Seguridad Clínica")
    
    # Regla 1: Protección para estadios avanzados
    if estadio_clinico in ["Estadio III", "Estadio IV (Metastásico)"] and not tiene_regenerativo:
        st.warning(
            f"⚠️ **Alerta de Estadio Avanzado ({estadio_clinico}):** "
            "Se detecta alta carga tumoral o riesgo sistémico. Se sugiere evaluar la incorporación "
            "de un compuesto de **Terapia Regenerativa / Inmunomoduladora** para mitigar el agotamiento celular."
        )
    elif estadio_clinico in ["Estadio III", "Estadio IV (Metastásico)"] and tiene_regenerativo:
        st.success("✅ **Soporte Regenerativo Presente:** El esquema cuenta con soporte celular para estadio avanzado.")
    else:
        st.info("ℹ️ **Estadio Temprano:** Monitoreo estándar activado.")

    # Regla 2: Verificación de presencia de tratamiento
    if df_activos.empty:
        st.error("🚨 **Sin Tratamiento Activo:** No se han activado compuestos en la grilla. El tumor crecerá de forma descontrolada.")

with col_val2:
    st.markdown("##### ⚡ Análisis de Sinergia Tri-Pilar")
    if aplica_sinergia:
        st.success(
            "🌟 **Sinergia Integrativa Detectada (+25%):** "
            "La coexistencia validada de **Soporte Químico** y **Apoyo Natural** potencia el coeficiente "
            "de reducción tumoral en la ecuación matemática."
        )
    else:
        st.info(
            "💡 **Sinergia Inactiva:** Para activar el bonus de sinergia integrativa (+25%), mantenga activo "
            "al menos un compuesto en **Soporte Químico** y uno en **Apoyo Natural** con eficacia > 0."
        )

# ==========================================
# 6. MOTOR MATEMÁTICO (SIMULACIÓN DE GOMPERTZ)
# ==========================================
# Cálculo de la tasa de remisión combinada
# Suma ponderada de (Eficacia * Dosis normalizada)
efectividad_base = 0.0
for _, row in df_activos.iterrows():
    # Normalización del efecto dosis/eficacia
    efectividad_base += (row["Eficacia Teórica (0.0 - 1.0)"] * (row["Dosis Diaria (mg)"] / 100.0))

efectividad_total = efectividad_base * factor_sinergia

# Arreglos para la simulación
dias = np.arange(0, dias_simulacion + 1)
volumen_control = np.zeros(len(dias))
volumen_tratado = np.zeros(len(dias))

# Condiciones iniciales
volumen_control[0] = volumen_inicial
volumen_tratado[0] = volumen_inicial

# Bucle de integración discreta día a día (Ecuación de Gompertz)
# dV/dt = r * V * ln(K / V) - (Efectividad * V)
for t in range(0, dias_simulacion):
    # 1. Tumor Control (Sin tratamiento)
    Vc = volumen_control[t]
    if Vc < capacidad_carga and Vc > 0:
        dV_control = tasa_crecimiento * Vc * np.log(capacidad_carga / Vc)
    else:
        dV_control = 0
    volumen_control[t + 1] = max(0.0, Vc + dV_control)

    # 2. Gemelo Digital Tratado (Con esquema integrativo)
    Vt = volumen_tratado[t]
    if Vt > 0.001:
        # Crecimiento Gompertziano natural
        if Vt < capacidad_carga:
            crecimiento_g = tasa_crecimiento * Vt * np.log(capacidad_carga / Vt)
        else:
            crecimiento_g = 0
        
        # Remisión por tratamiento
        remision_farmaco = efectividad_total * 0.05 * Vt
        
        dV_tratado = crecimiento_g - remision_farmaco
        volumen_tratado[t + 1] = max(0.0, Vt + dV_tratado)
    else:
        volumen_tratado[t + 1] = 0.0

# ==========================================
# 7. VISUALIZACIÓN GRÁFICA Y METRICAS KPI
# ==========================================
st.divider()
st.subheader("📈 Proyección del Gemelo Digital Tumoral")

col_graf, col_kpi = st.columns([3, 1])

with col_graf:
    # Gráfica interactiva con Plotly
    fig = go.Figure()

    # Curva Control
    fig.add_trace(go.Scatter(
        x=dias, y=volumen_control,
        mode='lines',
        name='Control (Sin Tratamiento)',
        line=dict(color='#EF4444', width=2, dash='dash')
    ))

    # Curva Tratada
    fig.add_trace(go.Scatter(
        x=dias, y=volumen_tratado,
        mode='lines',
        name=f'Gemelo Digital Tratado ({diagnostico_cancer})',
        line=dict(color='#10B981', width=3)
    ))

    fig.update_layout(
        title=f"Evolución del Volumen Tumoral en {dias_simulacion} Días",
        xaxis_title="Días de Tratamiento",
        yaxis_title="Volumen Tumoral (cm³)",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template="plotly_white",
        height=420
    )

    st.plotly_chart(fig, use_container_width=True)

with col_kpi:
    st.markdown("##### 📊 Indicadores Clave (KPIs)")
    
    vol_final_control = volumen_control[-1]
    vol_final_tratado = volumen_tratado[-1]
    porcentaje_reduccion = ((vol_final_control - vol_final_tratado) / vol_final_control) * 100 if vol_final_control > 0 else 0

    st.metric(
        label="Volumen Final Tratado",
        value=f"{vol_final_tratado:.2f} cm³",
        delta=f"-{porcentaje_reduccion:.1f}% vs Control",
        delta_color="normal"
    )

    st.metric(
        label="Volumen Inicial (V₀)",
        value=f"{volumen_inicial:.1f} cm³"
    )

    st.metric(
        label="Factor de Sinergia Aplicado",
        value=f"{'1.25 (+25%)' if aplica_sinergia else '1.00 (Base)'}"
    )

    if vol_final_tratado < 0.1:
        st.success("🎯 **Remisión Tumoral Completa Alcanzada**")
    elif vol_final_tratado < volumen_inicial:
        st.info("📉 **Respuesta Parcial / Regresión**")
    else:
        st.error("📈 **Enfermedad Progresiva / Crecimiento**")

# ==========================================
# 8. AUDITORÍA DETALLADA Y DESCARGA DE INFORME
# ==========================================
with st.expander("📄 Ver Resumen Clínico Detallado e Exportar Datos"):
    st.markdown(f"**Paciente:** {nombre_paciente} | **Edad:** {edad_paciente} | **Diagnóstico:** {diagnostico_cancer} ({estadio_clinico})")
    
    # Tabla resumen de proyección
    df_resultado = pd.DataFrame({
        "Día": dias,
        "Volumen_Control_cm3": np.round(volumen_control, 3),
        "Volumen_Tratado_cm3": np.round(volumen_tratado, 3)
    })
    
    st.dataframe(df_resultado.head(10), use_container_width=True)
    
    csv_bytes = df_resultado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Simulación Completa (CSV)",
        data=csv_bytes,
        file_name=f"simulacion_oncotwin_{nombre_paciente.replace(' ', '_')}.csv",
        mime="text/csv"
    )

st.caption("OncoTwin v2.5 — Plataforma conceptual para investigación, simulación biomédica y análisis de datos integrativos.")
    
