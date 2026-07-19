import streamlit as st
import pandas as pd
import numpy as np

# =====================================================================
# 1. CONFIGURACIÓN DE PARÁMETROS BIOLÓGICOS (Prevalencia en Chile)
# =====================================================================
# Definimos los 10 cánceres con sus tasas intrínsecas de crecimiento (r)
# y capacidades de carga volumétrica del tumor (K) para evitar KeyErrors.
CANCER_DATABASE = {
    "Cáncer de Próstata": {"r": 0.04, "K": 1000.0, "descripcion": "Mayor incidencia en hombres en Chile."},
    "Cáncer de Mama": {"r": 0.06, "K": 1200.0, "descripcion": "Principal causa de muerte oncológica en mujeres chilenas."},
    "Cáncer Colorrectal": {"r": 0.07, "K": 1400.0, "descripcion": "Alta prevalencia en ambos sexos por factores dietéticos."},
    "Cáncer Gástrico": {"r": 0.09, "K": 1300.0, "descripcion": "De alta letalidad y fuerte impacto epidemiológico nacional."},
    "Cáncer de Vesícula Biliar": {"r": 0.11, "K": 1100.0, "descripcion": "Prevalencia excepcionalmente alta en la población chilena."},
    "Cáncer de Pulmón": {"r": 0.10, "K": 1500.0, "descripcion": "Asociado a alta mortalidad y diagnóstico tardío."},
    "Cáncer de Ovarios": {"r": 0.08, "K": 1250.0, "descripcion": "Incorporado para perfilamiento y optimización de terapias ginecológicas."},
    "Cáncer Cervicouterino": {"r": 0.05, "K": 950.0, "descripcion": "Impacto crítico en salud pública y tamizaje preventivo."},
    "Cáncer de Riñón": {"r": 0.06, "K": 1150.0, "descripcion": "Incidencia en aumento sostenido en la última década."},
    "Linfoma No Hodgkin": {"r": 0.12, "K": 1600.0, "descripcion": "Comportamiento sistémico de rápido crecimiento hematológico."}
}

PILARE_OPTIONS = ["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"]

# =====================================================================
# 2. INTERFAZ DE USUARIO (Streamlit UI)
# =====================================================================
st.set_page_config(page_title="OncoTwin: Gemelo Digital Oncológico", layout="wide", page_icon="🧬")

st.title("🧬 OncoTwin: Gemelo Digital Pro")
st.subheader("Plataforma Multi-Cáncer y Motor de Validación Cruzada Integrativa (Chile)")
st.markdown("---")

# Layout de dos columnas principales
col_izquierda, col_derecha = st.columns([1, 2])

with col_izquierda:
    st.header("📋 Panel de Perfilamiento Clínico")
    
    paciente_nombre = st.text_input("Nombre del Paciente:", value="Paciente Referencia")
    
    # Selector de los 10 tipos de cáncer
    cancer_seleccionado = st.selectbox(
        "Diagnóstico Oncológico:", 
        options=list(CANCER_DATABASE.keys())
    )
    
    # Mostrar descripción epidemiológica dinámica
    st.caption(f"ℹ️ *{CANCER_DATABASE[cancer_seleccionado]['descripcion']}*")
    
    estadio_clinico = st.selectbox(
        "Estadio Clínico:",
        options=["Estadio I", "Estadio II", "Estadio III", "Estadio IV"]
    )
    
    volumen_inicial = st.slider("Volumen Tumoral Inicial ($V_0$ en $cm^3$):", min_value=10.0, max_value=300.0, value=100.0, step=5.0)

# =====================================================================
# 3. GRILLA INTERACTIVA DE COMPUESTOS (df_grilla)
# =====================================================================
with col_derecha:
    st.header("📊 Protocolo de Tratamiento (Grilla Dinámica)")
    st.markdown("Modifica, agrega o elimina compuestos. El gemelo digital recalculará la curva automáticamente.")

    # Datos base poblados con ejemplos claros de los 3 pilares activos
    if 'data_protocolo' not in st.session_state:
        st.session_state.data_protocolo = pd.DataFrame([
            {"Compuesto": "Quimioterapia Base", "Pilar de Tratamiento": "Soporte Químico", "Dosis (mg/día)": 400, "Eficacia Base (%)": 45.0},
            {"Compuesto": "Extracto Botánico Activo", "Pilar de Tratamiento": "Apoyo Natural", "Dosis (mg/día)": 200, "Eficacia Base (%)": 10.0},
            {"Compuesto": "Péptidos de Regeneración", "Pilar de Tratamiento": "Terapia Regenerativa", "Dosis (mg/día)": 50, "Eficacia Base (%)": 15.0}
        ])

    # Grilla editable usando st.data_editor
    df_editado = st.data_editor(
        st.session_state.data_protocolo,
        num_rows="dynamic",
        column_config={
            "Pilar de Tratamiento": st.column_config.SelectboxColumn(
                "Pilar de Tratamiento",
                help="Clasificación del compuesto dentro de OncoTwin",
                options=PILARE_OPTIONS,
                required=True,
            ),
            "Dosis (mg/día)": st.column_config.NumberColumn(min_value=0, max_value=2000, step=10),
            "Eficacia Base (%)": st.column_config.NumberColumn(min_value=0.0, max_value=100.0, step=1.0)
        },
        use_container_width=True,
        key="editor_protocolo"
    )

    # Actualizar estado de la sesión
    st.session_state.data_protocolo = df_editado

# =====================================================================
# 4. MOTOR DE VALIDACIÓN CRUZADA Y AUDITORÍA BIOLÓGICA
# =====================================================================
st.markdown("---")
st.header("🛡️ Auditoría del Motor de Validación Cruzada")

# Extraer pilares activos ingresados por el usuario
pilares_activos = df_editado["Pilar de Tratamiento"].dropna().tolist() if not df_editado.empty else []

tiene_quimico = "Soporte Químico" in pilares_activos
tiene_natural = "Apoyo Natural" in pilares_activos
tiene_regenerativo = "Terapia Regenerativa" in pilares_activos

# Espacio de Alertas en la Interfaz
alertas_detectadas = 0

# Regla 1: Protección en Estadios Avanzados
if estadio_clinico in ["Estadio III", "Estadio IV"] and not tiene_regenerativo:
    st.warning(f"⚠️ **Advertencia de Seguridad:** El paciente se encuentra en **{estadio_clinico}**. Se sugiere evaluar la incorporación de compuestos de **Terapia Regenerativa** celular para mitigar la degradación tisular severa.")
    alertas_detectadas += 1

# Regla 2: Sinergia Integradora Ausente
if tiene_quimico and not tiene_natural:
    st.info("💡 **Sugerencia de Optimización:** Se ha ingresado un agente de *Soporte Químico* (Tradicional) sin un coadyuvante de *Apoyo Natural*. Incorporar extractos botánicos validados podría mitigar efectos adversos y potenciar la respuesta citotóxica.")
    alertas_detectadas += 1

if alertas_detectadas == 0:
    st.success("✅ **Validación Exitosa:** El protocolo ingresado cumple con las directrices de coexistencia de pilares activos para el perfil clínico seleccionado.")

# =====================================================================
# 5. SIMULACIÓN MATEMÁTICA COHERENTE (Gompertz + Sinergia)
# =====================================================================
st.markdown("---")
st.header("📈 Proyección del Gemelo Digital (Simulación Matemática)")

# Parámetros del modelo según el tipo de cáncer elegido
params = CANCER_DATABASE[cancer_seleccionado]
r_base = params["r"]
K = params["K"]

# Calcular el impacto terapéutico total de la grilla
impacto_terapeutico_total = 0.0

if not df_editado.empty:
    for idx, fila in df_editado.iterrows():
        # Validar que la fila contenga datos válidos antes de operar
        if pd.notna(fila["Eficacia Base (%)"]) and pd.notna(fila["Dosis (mg/día)"]):
            # El impacto es proporcional a la eficacia y ponderado sutilmente por la dosis
            factor_dosis = min(fila["Dosis (mg/día)"] / 500.0, 1.5) # normalización referencial
            impacto_terapeutico_total += (fila["Eficacia Base (%)"] / 100.0) * factor_dosis

# Aplicación del BONUS MATEMÁTICO por Sinergia Integrativa
bonus_sinergia = 1.0
if tiene_quimico and tiene_natural:
    bonus_sinergia = 1.25  # Aumento del 25% en la efectividad del tratamiento combinado
    st.caption("✨ *Bonus Matemático por Sinergia Integrativa Aplicado (+25% de eficacia global en la curva).*")

# Ajuste del impacto final consolidado
impacto_final = beneficio_droga = impacto_terapeutico_total * bonus_sinergia

# Bucle de Simulación a 30 días
dias = 30
vector_tiempo = list(range(0, dias + 1))
vector_volumen = [volumen_inicial]

volumen_actual = volumen_inicial
for t in range(1, dias + 1):
    if volumen_actual > 0.1:
        # Ecuación logística discreta de Gompertz modificada:
        # dV/dt = r * V * ln(K/V) - (Impacto_Tratamiento * V)
        crecimiento = r_base * volumen_actual * np.log(K / volumen_actual)
        reduccion = beneficio_droga * 0.15 * volumen_actual # Factor de escala diario de remisión
        
        volumen_actual = volumen_actual + crecimiento - reduccion
        
        # Limitar el volumen para que no sea negativo ni supere la capacidad de carga espacial K
        volumen_actual = max(0.0, min(volumen_actual, K))
    else:
        volumen_actual = 0.0
        
    vector_volumen.append(volumen_actual)

# Preparar datos para el gráfico
df_grafico = pd.DataFrame({
    "Día de Simulación": vector_tiempo,
    "Volumen Tumoral (cm³)": vector_volumen
}).set_index("Día de Simulación")

# Despliegue visual del gráfico y las métricas
col_metricas, col_chart = st.columns([1, 2])

with col_metricas:
    st.metric(label="Volumen Inicial", value=f"{volumen_inicial:.1f} cm³")
    volumen_final = vector_volumen[-1]
    
    if volumen_final < volumen_inicial:
        st.metric(label="Volumen Final Proyectado (Día 30)", value=f"{volumen_final:.1f} cm³", delta=f"-{((volumen_inicial - volumen_final)/volumen_inicial)*100:.1f}% Remisión")
    else:
        st.metric(label="Volumen Final Proyectado (Día 30)", value=f"{volumen_final:.1f} cm³", delta=f"+{((volumen_final - volumen_inicial)/volumen_inicial)*100:.1f}% Progresión", delta_color="inverse")
        
    st.markdown(f"**Parámetros dinámicos aplicados:**\n"
                f"- Tasa de crecimiento ($r$): `{r_base}`\n"
                f"- Capacidad espacial máxima ($K$): `{K} cm³`")

with col_chart:
    st.line_chart(df_grafico)
