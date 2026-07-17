import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la interfaz gráfica de OncoTwin
st.set_page_config(page_title="OncoTwin Pro - Sistema Multi-Cáncer Chile", layout="wide", page_icon="🧬")

st.title("🧬 OncoTwin Pro: Gemelo Digital Oncológico")
st.subheader("Panel de Perfilamiento Clínico y Motor de Validación de Precisión")

# 1. Grilla Corregida: Los 10 Cánceres más Prevalentes en Chile (GLOBOCAN / MINSAL)
CANCERES_CHILE = [
    "Cáncer de Próstata",
    "Cáncer de Mama",
    "Cáncer Colorrectal",
    "Cáncer Gástrico (Estómago)",
    "Cáncer de Pulmón (Broncopulmonar)",
    "Cáncer de Vesícula Biliar",
    "Cáncer Cervicouterino (Cuello Uterino)",
    "Cáncer Renal (Riñón)",
    "Cáncer de Tiroides",
    "Cáncer de Ovarios (Epitelial)"
]

# --- CAPA VISUAL: PANEL DE PERFILAMIENTO DEL PACIENTE (SIDEBAR) ---
st.sidebar.header("📋 Datos de Perfilamiento del Paciente")

tipo_cancer = st.sidebar.selectbox("Tipo de Cáncer (Prevalencia Chile)", CANCERES_CHILE)
sexo = st.sidebar.radio("Sexo Biológico", ["Femenino", "Masculino"])
edad = st.sidebar.number_input("Edad", min_value=0, max_value=120, value=55)
estadio = st.sidebar.selectbox("Estadio Clínico", ["Estadio I", "Estadio II", "Estadio III", "Estadio IV"])

st.sidebar.subheader("🧬 Biomarcadores y Mutaciones")
mutaciones = st.sidebar.multiselect(
    "Seleccione mutaciones/biomarcadores detectados:",
    ["KRAS Mutado", "BRCA1 Mutado", "BRCA2 Mutado", "HER2 Positivo", "ER/PR Positivo", "Ninguna"],
    default=["Ninguna"]
)

st.sidebar.subheader("🏥 Comorbilidades y Alergias")
comorbilidades = st.sidebar.multiselect("Comorbilidades:", ["Hipertensión", "Insuficiencia Renal", "Ninguna"], default=["Ninguna"])
alergias = st.sidebar.text_input("Alergias a Medicamentos (Separadas por coma):", "Ninguna")


# --- CAPA DE LA GRILLA DE TRATAMIENTO A EVALUAR (INTERACTIVA) ---
st.write("### 💊 Grilla de Compuestos a Evaluar en la Simulación")
st.caption("Modifique las dosis, altere el factor nanométrico o añada nuevas filas dinámicamente.")

# Estructuración de datos en caché para no perder cambios del usuario al refrescar
if "df_grilla" not in st.session_state:
    datos_grilla = {
        "Producto / Compuesto": ["Olaparib", "Cetuximab", "Trastuzumab", "Extracto Botánico Adaptativo"],
        "Tipo": ["Fármaco Sintético", "Fármaco Sintético", "Fármaco Sintético", "Extracto Botánico"],
        "Dosis (mg/día)": [300, 400, 250, 50],
        "Factor Nanométrico": [True, False, True, True]
    }
    st.session_state.df_grilla = pd.DataFrame(datos_grilla)

# Renderizado de la grilla editable usando data_editor
df_editado = st.data_editor(st.session_state.df_grilla, num_rows="dynamic", use_container_width=True)


# --- CAPA DE VALIDACIÓN Y REVISIÓN DE INFORMACIÓN (LOGICA DE NEGOCIO) ---
st.write("### 🔍 Reporte de Auditoría y Validación Clínica")

def ejecutar_validacion_clinica(cancer, sex, muts, comorbs, df_compuestos, str_alergias):
    alertas_criticas = []
    advertencias = []
    validaciones_exitosas = []
    
    # Capa 1: Validación de Consistencia Biológica (Sexo vs. Diagnóstico)
    if cancer in ["Cáncer de Ovarios (Epitelial)", "Cáncer Cervicouterino (Cuello Uterino)"] and sex == "Masculino":
        alertas_criticas.append(f"❌ Inconsistencia Crítica: El **{cancer}** es anatómicamente incompatible con el sexo masculino.")
    elif cancer == "Cáncer de Próstata" and sex == "Femenino":
        alertas_criticas.append("❌ Inconsistencia Crítica: El **Cáncer de Próstata** es anatómicamente incompatible con el sexo femenino.")
    else:
        validaciones_exitosas.append("✅ Consistencia biológica de género y diagnóstico: Validada.")
        
    # Extraer y limpiar fármacos de la grilla para validación cruzada
    lista_compuestos = [str(c).strip().lower() for c in df_compuestos["Producto / Compuesto"].dropna().tolist()]
    lista_alergias = [a.strip().lower() for a in str_alergias.split(",") if a.strip()]
    
    # Validación inmediata de Alergias del Paciente
    for compuesto in lista_compuestos:
        if compuesto in lista_alergias:
            alertas_criticas.append(f"❌ Riesgo Inmunológico: El compuesto **{compuesto.capitalize()}** está registrado en las alergias del paciente.")

    # Capa 2: Validación de Biomarcadores (Mutaciones vs. Fármacos en la grilla)
    # Caso Requerido: Cáncer de Ovarios
    if cancer == "Cáncer de Ovarios (Epitelial)":
        if "BRCA1 Mutado" in muts or "BRCA2 Mutado" in muts:
            validaciones_exitosas.append("🧬 Mutación BRCA detectada: El uso de Inhibidores de PARP (*Olaparib*) es clínicamente idóneo.")
            if "olaparib" not in lista_compuestos:
                advertencias.append("⚠️ Sugerencia: Se detectó mutación BRCA, pero no ha agregado *Olaparib* a la grilla de simulación.")
        else:
            if "olaparib" in lista_compuestos:
                advertencias.append("⚠️ Eficacia Mitigada: Ha incluido *Olaparib* en la grilla sin registrar mutaciones de reparación homóloga (BRCA1/2).")
                
    # Caso Heredado: Cáncer Colorrectal
    elif cancer == "Cáncer Colorrectal":
        if "KRAS Mutado" in muts and "cetuximab" in lista_compuestos:
            alertas_criticas.append("❌ Resistencia Molecular Confirmada: *Cetuximab* está contraindicado en tumores con mutación KRAS activa.")
        elif "KRAS Mutado" not in muts and "cetuximab" in lista_compuestos:
            validaciones_exitosas.append("✅ Validación molecular: Estado KRAS nativo compatible con terapia anti-EGFR.")

    # Caso Adicional: Cáncer de Mama
    elif cancer == "Cáncer de Mama":
        if "HER2 Positivo" in muts and "trastuzumab" in lista_compuestos:
            validaciones_exitosas.append("✅ Terapia dirigida correcta: *Trastuzumab* validado para perfil molecular sobreexpresado.")
        elif "HER2 Positivo" not in muts and "trastuzumab" in lista_compuestos:
            advertencias.append("⚠️ Validación molecular: El anticuerpo *Trastuzumab* carece de diana terapéutica activa en fenotipos HER2-.")

    # Capa 3: Validación de Toxicidades Cruzadas (Medicina Integrada)
    if "Insuficiencia Renal" in comorbs:
        nefrotoxicos = ["olaparib", "cetuximab"]
        for fármaco in nefrotoxicos:
            if fármaco in lista_compuestos:
                advertencias.append(f"⚠️ Riesgo de Nefrotoxicidad: El aclaramiento renal de **{fármaco.capitalize()}** se verá comprometido por la insuficiencia. Considere disminuir la dosis.")

    return alertas_criticas, advertencias, validaciones_exitosas


# Ejecutar el motor de auditoría clínica en base al estado de la interfaz
alertas, advertencias, exitos = ejecutar_validacion_clinica(tipo_cancer, sexo, mutaciones, comorbilidades, df_editado, alergias)

# Renderizado condicional del estado del motor de validación
if alertas:
    for a in alertas:
        st.error(a)
    st.button("🚀 Ejecutar Simulación en Gemelo Digital", disabled=True, help="Resuelva los errores críticos de validación biológica para poder simular.")
else:
    st.success("🔒 Capa de datos validada. Sin inconsistencias críticas que bloqueen la simulación.")
    
    if advertencias:
        for adv in advertencias:
            st.warning(adv)
            
    if exitos:
        with st.expander("Ver verificaciones biológicas exitosas"):
            for ex in exitos:
                st.info(ex)

    # --- CAPA ANALÍTICA: MODELO MATEMÁTICO DE SIMULACIÓN DE TRATAMIENTO (GOMPERTZ) ---
    st.write("---")
    if st.button("🚀 Ejecutar Simulación en Gemelo Digital"):
        st.subheader(f"📈 Proyección Dinámica de Masa Tumoral para: {tipo_cancer}")
        
        # Constantes fisiológicas iniciales del Gemelo Digital
        dias = 30
        V0 = 100.0  # Volumen tumoral inicial en mm³
        r = 0.12    # Tasa intrínseca de crecimiento celular
        K = 1000.0  # Capacidad de carga biológica máxima del entorno espacial
        
        # Procesamiento dinámico de los fármacos ingresados en la grilla por el usuario
        efectividad_combinada = 0.0
        
        for idx, row in df_editado.iterrows():
            compuesto = str(row["Producto / Compuesto"]).lower().strip()
            dosis = float(row["Dosis (mg/día)"]) if pd.notnull(row["Dosis (mg/día)"]) else 0.0
            factor_nano = bool(row["Factor Nanométrico"]) if pd.notnull(row["Factor Nanométrico"]) else False
            
            coeficiente_base = 0.0002  # Fracción de remisión tumoral por miligramo
            
            # Penalizaciones de efectividad matemática basadas en la validación previa de biomarcadores
            if tipo_cancer == "Cáncer de Ovarios (Epitelial)" and compuesto == "olaparib" and "BRCA1 Mutado" not in mutaciones and "BRCA2 Mutado" not in mutaciones:
                coeficiente_base *= 0.1  # Reducción drástica del efecto farmacológico
            if tipo_cancer == "Cáncer de Mama" and compuesto == "trastuzumab" and "HER2 Positivo" not in mutaciones:
                coeficiente_base *= 0.05
                
            # Sinergia del Factor Nanométrico Adaptativo (Incrementa la penetración celular un 40%)
            if factor_nano:
                coeficiente_base *= 1.4
                
            efectividad_combinada += coeficiente_base * dosis
            
        # Simulación discreta temporal aplicando la ecuación de Gompertz modificada:
        # dV/dt = r * V * ln(K/V) - (Eficacia * Dosis * V)
        volumenes = [V0]
        v_actual = V0
        
        for t in range(1, dias):
            if v_actual > 1.0:
                crecimiento = r * v_actual * np.log(K / v_actual)
                remision = efectividad_combinada * v_actual
                v_siguiente = v_actual + (crecimiento - remision)
                v_siguiente = max(0.0, min(v_siguiente, K))  # Control de límites fisiológicos
            else:
                v_siguiente = 0.0
            volumenes.append(v_siguiente)
            v_actual = v_siguiente
            
        # Creación del DataFrame de la trayectoria para el gráfico
        df_simulacion = pd.DataFrame({
            "Día": list(range(dias)),
            "Volumen Tumoral (mm³)": volumenes
        }).set_index("Día")
        
        # Renderizado del gráfico dinámico lineal
        st.line_chart(df_simulacion)
        
        # Visualización de KPIs Clínicos finales
        col1, col2, col3 = st.columns(3)
        col1.metric("Volumen Inicial", f"{V0} mm³")
        col2.metric("Volumen Final (Día 30)", f"{round(volumenes[-1], 2)} mm³")
        reduccion = round(((V0 - volumenes[-1]) / V0) * 100, 2)
        col3.metric("Porcentaje de Reducción", f"{reduccion} %" if reduccion >= 0 else f"Crecimiento Anómalo: {abs(reduccion)} %")
        
