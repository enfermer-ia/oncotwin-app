import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="OncoTwin - Gemelo Digital Oncológico",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 1. INICIALIZACIÓN DEL ESTADO DE SESIÓN (SESSION STATE)
# ---------------------------------------------------------
if "df_tratamientos" not in st.session_state:
    st.session_state.df_tratamientos = pd.DataFrame({
        "Compuesto": ["Cisplatino", "Extracto Cúrcuma (Curcumina)", "Péptidos Biológicos"],
        "Pilar": ["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"],
        "Dosis (mg)": [50.0, 250.0, 100.0],
        "Eficacia": [0.0040, 0.0015, 0.0010]
    })

# Lista actualizada: 10 Cánceres más prevalentes en Chile
CANCERES_CHILE = [
    "Cáncer de Próstata",
    "Cáncer de Mama",
    "Cáncer Colorrectal",
    "Cáncer Gástrico (Estómago)",
    "Cáncer de Pulmón",
    "Cáncer de Vesícula Biliar",
    "Cáncer Cérvico-Uterino",
    "Cáncer de Ovarios",
    "Cáncer Renal",
    "Cáncer de Tiroides"
]

# ---------------------------------------------------------
# 2. BARRA LATERAL: PERFILAMIENTO CLÍNICO Y PARÁMETROS
# ---------------------------------------------------------
st.sidebar.header("🧬 Perfilamiento Clínico del Paciente")

tipo_cancer = st.sidebar.selectbox(
    "Diagnóstico (Prevalencia Chile):",
    CANCERES_CHILE,
    index=2  # Cáncer Colorrectal por defecto
)

estadio = st.sidebar.selectbox(
    "Estadio Clínico:",
    ["Estadio I", "Estadio II", "Estadio III", "Estadio IV"],
    index=2
)

edad = st.sidebar.slider("Edad del Paciente (Años):", 18, 90, 58)

st.sidebar.divider()
st.sidebar.header("⚙️ Parámetros de Simulación Tumoral")

V0 = st.sidebar.number_input("Volumen Tumoral Inicial V0 (cm³):", min_value=1.0, max_value=500.0, value=100.0, step=5.0)
K = st.sidebar.number_input("Capacidad de Carga K (cm³):", min_value=100.0, max_value=2000.0, value=1000.0, step=50.0)
r = st.sidebar.slider("Tasa Crecimiento Intrínseco (r):", 0.01, 0.20, 0.05, step=0.01)
dias = st.sidebar.slider("Días de Simulación:", 30, 180, 60)

if st.sidebar.button("🔄 Restablecer Grilla Inicial"):
    st.session_state.df_tratamientos = pd.DataFrame({
        "Compuesto": ["Cisplatino", "Extracto Cúrcuma (Curcumina)", "Péptidos Biológicos"],
        "Pilar": ["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"],
        "Dosis (mg)": [50.0, 250.0, 100.0],
        "Eficacia": [0.0040, 0.0015, 0.0010]
    })
    st.rerun()

# ---------------------------------------------------------
# 3. ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
st.title("🧬 OncoTwin: Gemelo Digital Oncológico")
st.markdown(f"**Perfil de Paciente:** {edad} años | **Diagnóstico:** {tipo_cancer} | **Estado:** {estadio}")
st.divider()

# ---------------------------------------------------------
# 4. GRILLA INTERACTIVA DE TRATAMIENTOS (3 PILARES)
# ---------------------------------------------------------
st.subheader("📋 Panel de Tratamientos y Pilares Activos")
st.caption("Edita, agrega o elimina compuestos. El motor matemático y la validación biológica se reajustan automáticamente al cambiar los datos.")

df_editado = st.data_editor(
    st.session_state.df_tratamientos,
    num_rows="dynamic",
    use_container_width=True,
    key="editor_tratamientos",
    column_config={
        "Compuesto": st.column_config.TextColumn("Compuesto / Fármaco", required=True),
        "Pilar": st.column_config.SelectboxColumn(
            "Pilar de Tratamiento",
            options=["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"],
            required=True
        ),
        "Dosis (mg)": st.column_config.NumberColumn("Dosis (mg)", min_value=0.0, max_value=2000.0, step=10.0, required=True),
        "Eficacia": st.column_config.NumberColumn("Eficacia Terapéutica (0 a 0.05)", min_value=0.0, max_value=0.05, step=0.0005, format="%.4f", required=True)
    }
)

# Sincronizar grilla con el estado de la sesión
st.session_state.df_tratamientos = df_editado

# ---------------------------------------------------------
# 5. SANITIZACIÓN Y LIMPIEZA DE DATOS (PREVIENE BUGS MATEMÁTICOS)
# ---------------------------------------------------------
df_valido = df_editado.copy()
df_valido = df_valido.dropna(subset=["Compuesto", "Pilar"])
df_valido["Dosis (mg)"] = pd.to_numeric(df_valido["Dosis (mg)"], errors="coerce").fillna(0.0)
df_valido["Eficacia"] = pd.to_numeric(df_valido["Eficacia"], errors="coerce").fillna(0.0)

# ---------------------------------------------------------
# 6. MOTOR DE VALIDACIÓN CRUZADA Y AUDITORÍA BIOLÓGICA
# ---------------------------------------------------------
st.divider()
st.subheader("🛡️ Motor de Validación Cruzada")

pilares_presentes = set(df_valido["Pilar"].dropna().tolist())
tiene_quimico = "Soporte Químico" in pilares_presentes
tiene_natural = "Apoyo Natural" in pilares_presentes
tiene_regenerativo = "Terapia Regenerativa" in pilares_presentes

col_val1, col_val2 = st.columns(2)

with col_val1:
    if tiene_quimico and tiene_natural:
        st.success("✨ **Sinergia Integrativa Detectada:** Coexisten compuestos de Soporte Químico y Apoyo Natural. Se aplica un **bonus de sinergia (+25%)** en el cálculo matemático.")
        bonus_sinergia = 1.25
    elif tiene_quimico:
        st.info("ℹ️ **Soporte Químico Activo:** Fármaco cito-reductivo directo sin modulación natural.")
        bonus_sinergia = 1.0
    else:
        st.warning("⚠️ **Sin Soporte Químico:** No hay fármacos cito-reductivos principales ingresados.")
        bonus_sinergia = 1.0

with col_val2:
    if estadio in ["Estadio III", "Estadio IV"] and not tiene_regenerativo:
        st.warning(f"🚨 **Advertencia Clínica ({estadio}):** En etapas avanzadas de {tipo_cancer}, se sugiere incorporar **Terapia Regenerativa** para proteger la masa de tejido sano.")
    elif tiene_regenerativo:
        st.success("🛡️ **Soporte Regenerativo Incluido:** Terapia de protección celular activa.")
    else:
        st.info("ℹ️ Perfil actual sin requerimiento estricto de soporte regenerativo crítico.")

# ---------------------------------------------------------
# 7. MOTOR MATEMÁTICO DE SIMULACIÓN (MODELO DE GOMPERTZ)
# ---------------------------------------------------------
# Cálculo del efecto total acumulado
efecto_por_compuesto = df_valido["Dosis (mg)"] * df_valido["Eficacia"]
efecto_total = efecto_por_compuesto.sum() * bonus_sinergia

# Bucle discreto de simulación día a día
volumenes = [float(V0)]
V_actual = float(V0)

for t in range(1, dias):
    if V_actual > 0.001:
        # Modelo Gompertz: dV/dt = r * V * ln(K/V) - (Efecto_Total * V)
        dV = (r * V_actual * np.log(K / V_actual)) - (efecto_total * V_actual)
        V_actual = max(0.0, V_actual + dV)
    else:
        V_actual = 0.0
    volumenes.append(V_actual)

df_simulacion = pd.DataFrame({
    "Día": list(range(dias)),
    "Volumen Tumoral (cm³)": volumenes
})

# ---------------------------------------------------------
# 8. RENDERIZADO Y GRÁFICO Plotly REACTIVO
# ---------------------------------------------------------
st.divider()
st.subheader("📈 Curva Evolutiva del Gemelo Digital")

volumen_final = volumenes[-1]
reduccion_pct = ((V0 - volumen_final) / V0) * 100.0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Volumen Inicial V0", f"{V0:.1f} cm³")
m2.metric(f"Volumen Final (Día {dias})", f"{volumen_final:.1f} cm³")
m3.metric("Cambio de Masa Tumoral", f"{reduccion_pct:+.1f} %", delta_color="inverse")
m4.metric("Sinergia Aplicada", f"{bonus_sinergia:.2f}x")

fig = px.line(
    df_simulacion,
    x="Día",
    y="Volumen Tumoral (cm³)",
    title=f"Evolución Tumoral: {tipo_cancer} ({estadio}) | Efecto Total de Tratamiento: {efecto_total:.4f}",
    labels={"Día": "Días de Simulación", "Volumen Tumoral (cm³)": "Volumen (cm³)"},
    template="plotly_white"
)
fig.update_traces(line_color="#E74C3C", line_width=3)
fig.add_hline(y=K, line_dash="dash", line_color="gray", annotation_text=f"Capacidad Carga K ({K} cm³)")

st.plotly_chart(fig, use_container_width=True)

# Tabla resumida de aporte individual
if not df_valido.empty:
    with st.expander("🔍 Ver Desglose de Aporte por Compuesto"):
        df_valido["Aporte Terapéutico"] = df_valido["Dosis (mg)"] * df_valido["Eficacia"]
        st.dataframe(df_valido[["Compuesto", "Pilar", "Dosis (mg)", "Eficacia", "Aporte Terapéutico"]], use_container_width=True)
