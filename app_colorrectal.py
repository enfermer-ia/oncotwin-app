import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la interfaz gráfica de OncoTwin
st.set_page_config(page_title="OncoTwin Pro - Sistema Multi-Cáncer Integrativo", layout="wide", page_icon="🧬")

st.title("🧬 OncoTwin Pro: Gemelo Digital Oncológico")
st.subheader("Panel de Perfilamiento Clínico y Motor de Validación Integrativa (Chile)")

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
edad = st.sidebar.number_input("Edad", min_value=0, max_value=120, value=56)
estadio = st.sidebar.selectbox("Estadio Clínico", ["Estadio I", "Estadio II", "Estadio III", "Estadio IV"])

st.sidebar.subheader("🧬 Biomarcadores y Mutaciones")
mutaciones = st.sidebar.multiselect(
    "Seleccione mutaciones/biomarcadores detectados:",
    ["KRAS Mutado", "BRCA1 Mutado", "BRCA2 Mutado", "HER2 Positivo", "ER/PR Positivo", "Ninguna"],
    default=["Ninguna"]
)

st.sidebar.subheader("🏥 Comorbilidades y Alergias")
comorbilidades = st.sidebar.multiselect("Comorbilidades:", ["Hipertensión", "Insuficiencia Renal", "Ninguna"], default=["Ninguna"])
alergias = st.sidebar.text_input("Alergias a Medicamentos / Compuestos (Separadas por coma):", "Ninguna")


# --- CAPA DE LA GRILLA DE TRATAMIENTO INTEGRATIVO (INTERACTIVA) ---
st.write("### 💊 Grilla de Intervención: Soporte Químico, Apoyo Natural y Terapia Regenerativa")
st.caption("Modifique las dosis, altere el factor nanométrico o añada nuevas filas dinámicamente. El sistema evaluará el impacto de cada pilar.")

# Inicialización de la grilla resguardando los 3 pilares originales de la aplicación
if "df_grilla" not in st.session_state:
    datos_grilla = {
        "Producto / Compuesto": [
            "Olaparib", 
            "Cetuximab", 
            "Extracto de Cúrcuma Concentrado", 
            "Extracto Botánico Adaptativo",
            "Terapia Celular Inmunomoduladora",
            "Factores de Crecimiento de Regeneración"
        ],
        "Pilar Terapéutico (Agente)": [
            "Soporte Químico", 
            "Soporte Químico", 
            "Apoyo Natural", 
            "Apoyo Natural",
            "Terapia Regenerativa",
            "Terapia Regenerativa"
        ],
        "Dosis (mg o unidades/día)": [300, 400, 500, 100, 50, 20],
        "Factor Nanométrico Adaptativo": [True, False, True, True, False, False]
    }
    st.session_state.df_grilla = pd.DataFrame(datos_grilla)

# Renderizado de la grilla interactiva editable
df_editado = st.data_editor(
    st.session_state.df_grilla, 
    num_rows="dynamic", 
    use_container_width=True,
    column_config={
        "Pilar Terapéutico (Agente)": st.column_config.SelectboxColumn(
            options=["Soporte Químico", "Apoyo Natural", "Terapia Regenerativa"],
            required=True
        )
    }
)


# --- CAPA DE VALIDACIÓN Y AUDITORÍA INTEGRATIVA EN TIEMPO REAL ---
st.write("### 🔍 Reporte del Motor de Validación Cruzada")

def ejecutar_validacion_clinica(cancer, sex, muts, comorbs, df_compuestos, str_alergias):
    alertas_criticas = []
    advertencias = []
    validaciones_exitosas = []
    
    # 1. Capa de Consistencia Biológica (Sexo vs. Diagnóstico de Prevalencia)
    if cancer in ["Cáncer de Ovarios (Epitelial)", "Cáncer Cervicouterino (Cuello Uterino)"] and sex == "Masculino":
        alertas_criticas.append(f"❌ Inconsistencia Crítica: El **{cancer}** es anatómicamente incompatible con el sexo masculino.")
    elif cancer == "Cáncer de Próstata" and sex == "Femenino":
        alertas_criticas.append("❌ Inconsistencia Crítica: El **Cáncer de Próstata** es anatómicamente incompatible con el sexo femenino.")
    else:
        validaciones_exitosas.append(f"✅ Consistencia biológica: Diagnóstico de {cancer} consistente con el sexo biológico.")
        
    # Extracción y estandarización de los compuestos ingresados dinámicamente en la grilla
    df_limpio = df_compuestos.dropna(subset=["Producto / Compuesto", "Pilar Terapéutico (Agente)"])
    lista_compuestos = [str(c).strip().lower() for c in df_limpio["Producto / Compuesto"].tolist()]
    lista_pilares = [str(p).strip() for p in df_limpio["Pilar Terapéutico (Agente)"].tolist()]
    lista_alergias = [a.strip().lower() for a in str_alergias.split(",") if a.strip()]
    
    # 2. Validación de Alergias Dinámicas
    for compuesto in lista_compuestos:
        if compuesto in lista_alergias:
            alertas_criticas.append(f"❌ Riesgo Inmunológico: El compuesto **{compuesto.capitalize()}** ingresado en la grilla figura en las alergias del paciente.")

    # 3. Validación Cruzada de Biomarcadores y Medicamentos (Soporte Químico)
    # Caso Cáncer de Ovarios (Solicitado)
    if cancer == "Cáncer de Ovarios (Epitelial)":
        if "BRCA1 Mutado" in muts or "BRCA2 Mutado" in muts:
            validaciones_exitosas.append("🧬 Biomarcador BRCA+: El uso de inhibidores de PARP (como Olaparib) es idóneo para este perfil.")
            if "olaparib" not in lista_compuestos:
                advertencias.append("⚠️ Sugerencia (Soporte Químico): Paciente tiene mutación BRCA, pero no se ha incluido *Olaparib* en la grilla.")
        else:
            if "olaparib" in lista_compuestos:
                advertencias.append("⚠️ Eficacia Mitigada: Ha incluido *Olaparib* sin mutaciones de reparación homóloga (BRCA1/2) detectadas.")
                
    # Caso Cáncer Colorrectal
    elif cancer == "Cáncer Colorrectal":
        if "KRAS Mutado" in muts and "cetuximab" in lista_compuestos:
            alertas_criticas.append("❌ Resistencia Molecular: El anticuerpo *Cetuximab* está contraindicado en Cáncer Colorrectal con mutación KRAS activa.")
        elif "KRAS Mutado" not in muts and "cetuximab" in lista_compuestos:
            validaciones_exitosas.append("✅ Validación molecular: Estado KRAS nativo compatible con terapia anti-EGFR.")

    # Caso Cáncer de Mama
    elif cancer == "Cáncer de Mama":
        if "HER2 Positivo" in muts and "trastuzumab" in lista_compuestos:
            validaciones_exitosas.append("✅ Diana Activa: *Trastuzumab* correctamente orientado al receptor HER2 sobreexpresado.")

    # 4. Validación de Sinergias (Apoyo Natural y Terapias Regenerativas)
    cont_natural = lista_pilares.count("Apoyo Natural")
    cont_quimico = lista_pilares.count("Soporte Químico")
    cont_regenerativo = lista_pilares.count("Terapia Regenerativa")
    
    if cont_quimico > 0 and cont_natural > 0:
        validaciones_exitosas.append(f"🌱 Sinergia Integrativa Detectada: El agente de **Apoyo Natural** ({cont_natural} compuestos) optimizará las vías metabólicas del **Soporte Químico**.")
    
    if estadio in ["Estadio III", "Estadio IV"]:
        if cont_regenerativo == 0:
            advertencias.append(f"⚠️ Recomendación de Manejo: En {estadio}, considere añadir compuestos de **Terapia Regenerativa** para mitigar la toxicidad celular y proteger el microambiente.")
        else:
            validaciones_exitosas.append("🛡️ Soporte Regenerativo Activo: Las terapias regenerativas seleccionadas ayudarán a la resiliencia de tejidos sanos.")

    if "Insuficiencia Renal" in comorbs and "olaparib" in lista_compuestos:
        advertencias.append("⚠️ Comorbilidad Crítica: El aclaramiento de *Olaparib* se reduce en insuficiencia renal. Supervise o ajuste dosis.")

    return alertas_criticas, advertencias, validaciones_exitosas


# Ejecutar auditoría del motor clínico
alertas, advertencias, exitos = ejecutar_validacion_clinica(tipo_cancer, sexo, mutaciones, comorbilidades, df_editado, alergias)

# Renderizado condicional basado en el estado clínico de los datos de la grilla
if alertas:
    for a in alertas:
        st.error(a)
    st.button("🚀 Ejecutar Simulación en Gemelo Digital", disabled=True, help="Solucione los conflictos o inconsistencias de la grilla para simular.")
else:
    st.success("🔒 Validación Integrativa aprobada. Listo para simulación analítica.")
    
    if advertencias:
        for adv in advertencias:
            st.warning(adv)
            
    if exitos:
        with st.expander("Ver verificaciones y sinergias exitosas"):
            for ex in exitos:
                st.info(ex)

    # --- CAPA ANALÍTICA: MODELO MATEMÁTICO DE SIMULACIÓN DE TRATAMIENTO (GOMPERTZ MULTI-PILAR) ---
    st.write("---")
    if st.button("🚀 Ejecutar Simulación en Gemelo Digital"):
        st.subheader(f"📈 Evolución de la Masa Tumoral simulada para: {tipo_cancer}")
        
        # Parámetros base del Gemelo Digital
        dias = 30
        V0 = 120.0  # Volumen tumoral inicial en mm³
        r = 0.15    # Tasa intrínseca de replicación celular
        K = 1200.0  # Capacidad de carga biológica límite espacio-temporal
        
        # Cálculo dinámico de la Eficacia Combinada recorriendo CADA FILA ingresada por el usuario
        efectividad_total = 0.0
        
        df_limpio = df_editado.dropna(subset=["Producto / Compuesto", "Pilar Terapéutico (Agente)"])
        
        for idx, row in df_limpio.iterrows():
            compuesto = str(row["Producto / Compuesto"]).lower().strip()
            pilar = str(row["Pilar Terapéutico (Agente)"]).strip()
            dosis = float(row["Dosis (mg o unidades/día)"]) if pd.notnull(row["Dosis (mg o unidades/día)"]) else 0.0
            factor_nano = bool(row["Factor Nanométrico Adaptativo"]) if pd.notnull(row["Factor Nanométrico Adaptativo"]) else False
            
            # Asignación de coeficientes base matemáticos según el Pilar/Agente
            if pilar == "Soporte Químico":
                coef_base = 0.00025
                # Penalizaciones biológicas por biomarcadores
                if tipo_cancer == "Cáncer de Ovarios (Epitelial)" and compuesto == "olaparib" and "BRCA1 Mutado" not in mutaciones and "BRCA2 Mutado" not in mutaciones:
                    coef_base *= 0.1
                if tipo_cancer == "Cáncer Colorrectal" and compuesto == "cetuximab" and "KRAS Mutado" in mutaciones:
                    coef_base *= 0.0
            elif pilar == "Apoyo Natural":
                coef_base = 0.00008  # Acción citostática indirecta o de bloqueo de vías metabólicas alternativas
            elif pilar == "Terapia Regenerativa":
                coef_base = 0.00004  # Inmunomodulación y reordenamiento del estroma tumoral
            else:
                coef_base = 0.00005
                
            # Sinergia por el Factor Nanométrico Adaptativo (Aumenta biodisponibilidad celular en un 40%)
            if factor_nano:
                coef_base *= 1.4
                
            efectividad_total += coef_base * dosis
            
        # Potenciación matemática por Sinergias Integrativas (Combinación de pilares)
        lista_pilares_activos = df_limpio["Pilar Terapéutico (Agente)"].tolist()
        if "Soporte Químico" in lista_pilares_activos and "Apoyo Natural" in lista_pilares_activos:
            efectividad_total *= 1.15  # Un 15% de bonus matemático en remisión por sinergia fármaco-botánica
        if "Terapia Regenerativa" in lista_pilares_activos and estadio in ["Estadio III", "Estadio IV"]:
            efectividad_total *= 1.08  # Un 8% de bonus por contención inmunológica celular en estadios avanzados

        # Simulación computacional de la ecuación diferencial de Gompertz modificada:
        # dV/dt = r * V * ln(K/V) - (Eficacia_total * V)
        volumenes = [V0]
        v_actual = V0
        
        for t in range(1, dias):
            if v_actual > 1.0:
                crecimiento = r * v_actual * np.log(K / v_actual)
                remision = efectividad_total * v_actual
                v_siguiente = v_actual + (crecimiento - remision)
                v_siguiente = max(0.0, min(v_siguiente, K))  # Limites biológicos de saturación
            else:
                v_siguiente = 0.0
            volumenes.append(v_siguiente)
            v_actual = v_siguiente
            
        # Conversión de la trayectoria de simulación a un DataFrame indexado por días
        df_simulacion = pd.DataFrame({
            "Día de Evaluación": list(range(dias)),
            "Masa Tumoral Estimada (mm³)": volumenes
        }).set_index("Día de Evaluación")
        
        # Gráfico dinámico interactivo en Streamlit
        st.line_chart(df_simulacion)
        
        # Despliegue de Indicadores Clave de Rendimiento Clínico (KPIs)
        col1, col2, col3 = st.columns(3)
        col1.metric("Volumen Tumoral Inicial", f"{V0} mm³")
        col2.metric("Volumen Final (Día 30)", f"{round(volumenes[-1], 2)} mm³")
        
        pct_reduccion = round(((V0 - volumenes[-1]) / V0) * 100, 2)
        if pct_reduccion >= 0:
            col3.metric("Porcentaje de Remisión Obtenido", f"{pct_reduccion} %")
        else:
            col3.metric("Progresión de la Enfermedad", f"+{abs(pct_reduccion)} %", delta_color="inverse")
    
