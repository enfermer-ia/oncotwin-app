import streamlit as st
import numpy as np
import pandas as pd

# Configuración principal de la interfaz de usuario
st.set_page_config(page_title="OncoTwin - Gemelo Digital Oncológico", layout="wide", page_icon="🧬")

st.title("🧬 OncoTwin: Gemelo Digital Oncológico")
st.write("Simulación interactiva basada en el crecimiento de Gompertz con auditoría clínica automatizada para Chile.")

# -------------------------------------------------------------------------
# 1. PANEL DE PERFILAMIENTO CLÍNICO (Grilla con el Top 10 de Cánceres en Chile)
# -------------------------------------------------------------------------
st.sidebar.header("📋 Panel de Perfilamiento Clínico")

# Lista expandida a los 10 cánceres más prevalentes en el país (incluyendo Ovarios)
lista_canceres_chile = [
    "Cáncer de Próstata",
    "Cáncer de Mama",
    "Cáncer Colorrectal",
    "Cáncer Gástrico (Estómago)",
    "Cáncer de Pulmón",
    "Cáncer de Vesícula Biliar",
    "Cáncer Cervicouterino",
    "Cáncer de Tiroides",
    "Cáncer Renal",
    "Cáncer de Ovarios"
]

tipo_cancer = st.sidebar.selectbox(
    "Seleccione el Diagnóstico Oncológico:",
    lista_canceres_chile
)

estadio_clinico = st.sidebar.selectbox(
    "Estadio Clínico del Paciente:",
    ["Estadio I", "Estadio II", "Estadio III", "Estadio IV"]
)

# Diccionario de parámetros clínicos base para ajustar la simulación según el tejido
parametros_onco = {
    "Cáncer de Próstata": {"r_base": 0.03, "K_base": 1000.0, "V0_base": 150.0},
    "Cáncer de Mama": {"r_base": 0.05, "K_base": 1200.0, "V0_base": 200.0},
    "Cáncer Colorrectal": {"r_base": 0.06, "K_base": 1500.0, "V0_base": 250.0},
    "Cáncer Gástrico (Estómago)": {"r_base": 0.08, "K_base": 1800.0, "V0_base": 300.0},
    "Cáncer de Pulmón": {"r_base": 0.09, "K_base": 2000.0, "V0_base": 350.0},
    "Cáncer de Vesícula Biliar": {"r_base": 0.07, "K_base": 1400.0, "V0_base": 220.0},
    "Cáncer Cervicouterino": {"r_base": 0.05, "K_base": 1100.0, "V0_base": 180.0},
    "Cáncer de Tiroides": {"r_base": 0.02, "K_base": 800.0, "V0_base": 100.0},
    "Cáncer Renal": {"r_base": 0.04, "K_base": 1300.0, "V0_base": 210.0},
    "Cáncer de Ovarios": {"r_base": 0.07, "K_base": 1600.0, "V0_base": 280.0}
}

config_base = parametros_onco[tipo_cancer]

# -------------------------------------------------------------------------
# 2. GRILLA INTERACTIVA DE TRATAMIENTO (Los 3 Pilares Activos)
# -------------------------------------------------------------------------
st.subheader("💊 Plan de Tratamiento Integrativo")
st.write("Configure los compuestos en base a los 3 pilares pilares fundamentales del tratamiento:")

# Inicialización del DataFrame por defecto dentro de st.session_state
if "df_grilla" not in st.session_state:
    data_inicial = {
        "Compuesto / Fármaco": ["Fármaco Quimioterapéutico", "Extracto Botánico Activo", "Factores de Regeneración"],
        "Pilar de Tratamiento": ["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"],
        "Dosis (mg/día)": [150.0, 400.0, 75.0],
        "Eficacia Estimada (0.00 - 1.00)": [0.30, 0.08, 0.04]
    }
    st.session_state.df_grilla = pd.DataFrame(data_inicial)

pilares_disponibles = ["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"]

# Renderizado dinámico de la tabla interactiva utilizando st.data_editor
df_editado = st.data_editor(
    st.session_state.df_grilla,
    num_rows="dynamic",
    column_config={
        "Pilar de Tratamiento": st.column_config.SelectboxColumn(
            "Pilar de Tratamiento",
            options=pilares_disponibles,
            required=True
        ),
        "Dosis (mg/día)": st.column_config.NumberColumn(min_value=0.0, step=10.0, format="%.1f"),
        "Eficacia Estimada (0.00 - 1.00)": st.column_config.NumberColumn(min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
    },
    key="editor_oncotwin"
)

# Guardamos el estado actual
st.session_state.df_grilla = df_editado

# -------------------------------------------------------------------------
# 3. MOTOR DE VALIDACIÓN CRUZADA Y AUDITORÍA BIOLÓGICA
# -------------------------------------------------------------------------
st.subheader("🛡️ Auditoría del Motor de Validación Cruzada")

# Validación Segura: Filtrado estricto eliminando nulos o filas vacías intermedias
df_auditable = df_editado.dropna(subset=["Pilar de Tratamiento", "Dosis (mg/día)", "Eficacia Estimada (0.00 - 1.00)"])
df_auditable = df_auditable[pd.notna(df_auditable["Pilar de Tratamiento"])]

# Evaluaciones lógicas de la terapia cargada
tiene_soporte_quimico = any(df_auditable["Pilar de Tratamiento"] == "Soporte Químico")
tiene_apoyo_natural = any(df_auditable["Pilar de Tratamiento"] == "Apoyo Natural")
tiene_terapia_regenerativa = any(df_auditable["Pilar de Tratamiento"] == "Terapia Regenerativa")

bonus_sinergia = 1.0  # Multiplicador base neutral

# Alerta 1: Sinergia Integrativa entre tradicional y fitoterapéutico
if tiene_soporte_quimico and tiene_apoyo_natural:
    st.success("✨ **Sinergia Integrativa Activa**: Se ha detectado la coexistencia de fármacos químicos con extractos naturales, aplicando un bonus matemático por potenciación en la curva gráfica.")
    bonus_sinergia = 1.20  # Aumenta un 20% la efectividad del tratamiento global
else:
    if tiene_soporte_quimico and not tiene_apoyo_natural:
        st.info("💡 **Recomendación**: Considere agregar compuestos de 'Apoyo Natural' para contrarrestar efectos adversos y optimizar la respuesta biológica.")

# Alerta 2: Alertas protectoras en Estadios Avanzados
if estadio_clinico in ["Estadio III", "Estadio IV"]:
    if not tiene_terapia_regenerativa:
        st.warning(f"⚠️ **Advertencia Protectora**: El paciente se encuentra en un estadio avanzado ({estadio_clinico}) y no se han ingresado terapias de 'Terapia Regenerativa' para resguardar la estabilidad celular.")
    else:
        st.success("✅ **Protección Tisular**: Terapia regenerativa correctamente considerada para estadios avanzados.")

# -------------------------------------------------------------------------
# 4. SIMULACIÓN MATEMÁTICA COHERENTE (Ecuación Discreta de Gompertz)
# -------------------------------------------------------------------------
st.subheader(f"📊 Curva de Evolución del Tumor: {tipo_cancer} ({estadio_clinico})")

# Cálculo dinámico del impacto acumulado de los fármacos en la grilla
impacto_terapeutico_total = 0.0
for _, fila in df_auditable.iterrows():
    dosis = fila["Dosis (mg/día)"]
    eficacia = fila["Eficacia Estimada (0.00 - 1.00)"]
    # Escalado simple para ponderar dosis y eficacia
    impacto_terapeutico_total += (eficacia * (dosis / 200.0))

# Inyección del bonus de sinergia determinado por la auditoría cruzada
impacto_terapeutico_total *= bonus_sinergia

# Ajustar parámetros de Gompertz según la agresividad del estadio clínico elegido
r_sim = config_base["r_base"]
K_sim = config_base["K_base"]
V0_sim = config_base["V0_base"]

if estadio_clinico == "Estadio II":
    r_sim *= 1.20
elif estadio_clinico == "Estadio III":
    r_sim *= 1.45
    V0_sim *= 1.40
elif estadio_clinico == "Estadio IV":
    r_sim *= 1.75
    V0_sim *= 1.80

# Bucle de iteración temporal
horizonte_temporal = 60  # Días evaluados en la gráfica
volumenes = [V0_sim]
dias = list(range(0, horizonte_temporal + 1))

V_t = V0_sim
for t in range(1, horizonte_temporal + 1):
    if V_t > 0.1:
        # dV/dt = r * V * ln(K/V) - (Efecto * V)
        crecimiento_gompertz = r_sim * V_t * np.log(K_sim / V_t)
        reduccion_tratamiento = impacto_terapeutico_total * V_t
        V_t = V_t + crecimiento_gompertz - reduccion_tratamiento
        if V_t < 0:
            V_t = 0.0
    else:
        V_t = 0.0
    volumenes.append(V_t)

# Creación del set de datos para graficar
df_simulacion = pd.DataFrame({
    "Día": dias,
    "Volumen Tumoral (mm³)": volumenes
}).set_index("Día")

# Renderizado de la gráfica de Streamlit
st.line_chart(df_simulacion)

# Sección de KPI informativos
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Volumen Inicial del Tumor", value=f"{V0_sim:.1f} mm³")
with col2:
    st.metric(label="Volumen Final Estimado (Día 60)", value=f"{volumenes[-1]:.1f} mm³")
with col3:
    variacion_porcentual = ((volumenes[-1] - V0_sim) / V0_sim) * 100
    st.metric(
        label="Efecto sobre el Crecimiento",
        value=f"{variacion_porcentual:.1f}%",
        delta=f"{variacion_porcentual:.1f}% (Reducción)" if variacion_porcentual <= 0 else f"+{variacion_porcentual:.1f}% (Progresión)",
        delta_color="inverse"
    )
    
