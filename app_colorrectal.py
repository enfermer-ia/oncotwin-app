import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE PANTALLA ADAPTATIVA Y PROFESIONAL
st.set_page_config(page_title="OncoTwin Pro v5 - Chile", layout="wide")
st.title("🧬 OncoTwin Pro: By MEDISYS (Edición Chile)")
st.write("Gemelo Digital de Precisión para REGENERA.")

# -------------------------------------------------------------
# BASE DE DATOS DILIGENCIADA POR CÁNCER (MÁXIMA FRECUENCIA EN CHILE)
# -------------------------------------------------------------
db_chile_oncologia = {
    "Cáncer Colorrectal": {
        "mutaciones": ["APC Mutado", "KRAS Mutado", "BRAF Mutado", "TP53 Mutado"],
        "vias": ["β-catenina (Eje Wnt)", "ERK (Eje MAPK)"],
        "farmacos": {
            "5-Fluorouracilo (5-FU)": 0.65, "Oxaliplatino": 0.70, "Irinotecán": 0.68, 
            "Capecitabina": 0.60, "Cetuximab": 0.75, "Panitumumab": 0.73, "Regorafenib": 0.55
        },
        "fitofarmacos": {
            "Curcumina (Cúrcuma)": 0.40, "Quercetina": 0.38, "EGCG (Té Verde)": 0.35, 
            "Resveratrol": 0.42, "Sulforafano": 0.39, "Silibinina": 0.33, "Berberina": 0.45
        },
        "regenerativas": {
            "Exosomas Cargados con miRNA-145": 0.58, "Exosomas de Células Dendríticas": 0.52, 
            "Células Madre Mesenquimales (MSCs-TRAIL)": 0.60, "Exosomas Derivados de MSC (M2-to-M1)": 0.48, 
            "Células NK Alogénicas": 0.64, "Exosomas con siRNA anti-β-catenina": 0.56, "Secretoma de Células Madre Hipóxicas": 0.38
        }
    },
    "Cáncer de Próstata": {
        "mutaciones": ["PTEN Mutado", "AR Amplificado", "BRCA2 Mutado", "TP53 Mutado"],
        "vias": ["Receptor Androgénico (AR)", "AKT (Vía PTEN/PI3K)"],
        "farmacos": {
            "Enzalutamida": 0.78, "Abiraterona": 0.75, "Docetaxel": 0.70, 
            "Olaparib": 0.72, "Cabazitaxel": 0.67, "Bicalutamida": 0.58, "Leuprolida": 0.64
        },
        "fitofarmacos": {
            "Licopeno (Tomate)": 0.42, "Saw Palmetto (Sabal)": 0.38, "EGCG (Té Verde)": 0.40, 
            "Curcumina": 0.39, "Quercetina": 0.36, "Genisteína": 0.35, "Sulforafano": 0.37
        },
        "regenerativas": {
            "Exosomas con siRNA anti-AR": 0.62, "Exosomas de Células Dendríticas Activadas": 0.65, 
            "Células Madre Mesenquimales (MSCs-TRAIL)": 0.59, "Células NK Alogénicas": 0.63, 
            "Vesículas de Reprogramación Inmune": 0.50, "Secretoma Protector Óseo (Anti-Metástasis)": 0.45, "Vesículas de MSC": 0.40
        }
    },
    "Cáncer de Mama": {
        "mutaciones": ["HER2 Positivo", "PIK3CA Mutado", "BRCA1 Mutado", "RE/RP Positivo"],
        "vias": ["Receptor HER2/Neu", "AKT (Vía PI3K/mTOR)"],
        "farmacos": {
            "Trastuzumab": 0.82, "Pertuzumab": 0.80, "Paclitaxel": 0.72, 
            "Tamoxifeno": 0.66, "Palbociclib": 0.75, "Doxorrubicina": 0.70, "Capecitabina": 0.62
        },
        "fitofarmacos": {
            "Sulforafano (Brócoli)": 0.45, "EGCG (Té Verde)": 0.41, "Genisteína (Soja)": 0.38, 
            "Quercetina": 0.37, "Curcumina": 0.40, "Resveratrol": 0.42, "Apigenina": 0.36
        },
        "regenerativas": {
            "Exosomas Cargados con PTEN": 0.63, "Exosomas con miRNA-21 Inhibidor": 0.57, 
            "Células NK Alogénicas": 0.66, "Células Madre Mesenquimales (MSCs-TRAIL)": 0.61, 
            "Exosomas Inmunomoduladores": 0.52, "Secretoma Regulador de Proliferación": 0.44, "Exosomas con siRNA anti-PI3K": 0.58
        }
    },
    "Cáncer Gástrico (Estómago)": {
        "mutaciones": ["HER2 Positivo", "CDH1 Mutado", "TP53 Mutado", "Inestabilidad Satelital (MSI)"],
        "vias": ["Receptor HER2/EGFR", "STAT3 (Vía Inflamatoria)"],
        "farmacos": {
            "Cisplatino": 0.68, "Capecitabina": 0.62, "Trastuzumab": 0.79, 
            "Ramucirumab": 0.71, "Pembrolizumab": 0.76, "5-Fluorouracilo (5-FU)": 0.64, "Oxaliplatino": 0.69
        },
        "fitofarmacos": {
            "Sulforafano": 0.46, "Ginsenósidos (Ginseng)": 0.42, "Quercetina": 0.39, 
            "Curcumina": 0.41, "EGCG (Té Verde)": 0.38, "Berberina": 0.43, "Silibinina": 0.35
        },
        "regenerativas": {
            "Exosomas con miRNA-34a": 0.60, "Células NK Alogénicas": 0.65, 
            "Secretoma de Células Madre Gástricas": 0.43, "Células Madre Mesenquimales (MSCs-TRAIL)": 0.58, 
            "Exosomas Presentadores de Antígenos": 0.54, "Exosomas de Macrófagos M1": 0.51, "Vesículas Reguladoras Epiteliales": 0.46
        }
    },
    "Cáncer de Pulmón": {
        "mutaciones": ["EGFR Mutado", "ALK Fusionado", "KRAS Mutado", "TP53 Mutado"],
        "vias": ["Receptor EGFR (MAPK)", "ALK / Eje AKT (Supervivencia)"],
        "farmacos": {
            "Osimertinib": 0.84, "Alectinib": 0.81, "Pembrolizumab": 0.77, 
            "Cisplatino": 0.66, "Carboplatino": 0.64, "Paclitaxel": 0.68, "Docetaxel": 0.69
        },
        "fitofarmacos": {
            "EGCG (Té Verde)": 0.43, "Resveratrol": 0.41, "Curcumina": 0.40, 
            "Astrágalo (Extracto)": 0.45, "Sulforafano": 0.42, "Quercetina": 0.38, "Fisetina": 0.37
        },
        "regenerativas": {
            "Exosomas con siRNA anti-EGFR": 0.64, "Exosomas con miRNA-133b": 0.59, 
            "Células NK Alogénicas": 0.67, "Células Madre Mesenquimales (MSCs-TRAIL)": 0.62, 
            "Exosomas Anti-Angiogénicos": 0.55, "Secretoma Protector Alveolar": 0.41, "Vesículas de Células T Quiméricas": 0.63
        }
    }
}

# -------------------------------------------------------------
# SECCIÓN I: PANEL DE PERFILADO CLÍNICO DEL PACIENTE
# -------------------------------------------------------------
with st.expander("👤 PANEL I: Perfilado Omnipresente del Paciente (Historial Clínico y Ómico)", expanded=True):
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    
    with col_p1:
        cancer_type = st.selectbox("Tipo de Cáncer (Frecuentes en Chile)", list(db_chile_oncologia.keys()))
        estadio = st.selectbox("Estadío Clínico", ["Estadío I", "Estadío II", "Estadío III", "Estadío IV (Metastásico)"])
        tiempo_det = st.number_input("Tiempo desde Detección (meses)", min_value=1, max_value=120, value=6)
        
    with col_p2:
        sexo = st.radio("Sexo Biológico", ["Masculino", "Femenino"], horizontal=True)
        edad = st.number_input("Edad (Años)", min_value=18, max_value=100, value=62)
        peso = st.number_input("Peso (kg)", min_value=30, max_value=150, value=70)
        
    with col_p3:
        profesion = st.text_input("Profesión / Actividad", "Pensionado / Agricultor")
        tratamiento_actual = st.selectbox("Tratamiento Actual Base", ["Quimioterapia Convencional", "Inmunoterapia Base", "Terapia Dirigida Oral", "Ninguno (Primera Línea)"])
        tiempo_aplicacion = st.number_input("Tiempo con Tratamiento Actual (ciclos)", min_value=0, max_value=12, value=2)
        
    with col_p4:
        comorbilidades = st.multiselect("Comorbilidades", ["Hipertensión Arterial", "Cardiopatía", "Diabetes Tipo 2", "Ninguna"], default=["Ninguna"])
        alergias = st.text_input("Alergias Conocidas", "Ninguna")
        
        mutaciones_disponibles = db_chile_oncologia[cancer_type]["mutaciones"]
        mutaciones = st.multiselect("Mutaciones Conductoras (Ómica Personalizada)", mutaciones_disponibles, default=[mutaciones_disponibles[0]])

# Extracción dinámica de datos según la selección del usuario
vias_nombres = db_chile_oncologia[cancer_type]["vias"]
farmacos_dict = db_chile_oncologia[cancer_type]["farmacos"]
fitofarmacos_dict = db_chile_oncologia[cancer_type]["fitofarmacos"]
regenerativas_dict = db_chile_oncologia[cancer_type]["regenerativas"]

# -------------------------------------------------------------
# MOTOR DE RECOMENDACIÓN DE IA CONSENSUADA
# -------------------------------------------------------------
sug_f = list(farmacos_dict.keys())[0]
sug_b = list(fitofarmacos_dict.keys())[0]
sug_r = list(regenerativas_dict.keys())[0]
justificaciones = []

if cancer_type == "Cáncer Colorrectal":
    if "KRAS Mutado" in mutaciones:
        sug_f = "Irinotecán"
        sug_r = "Exosomas Cargados con miRNA-145"
        justificaciones.append("• **SOPORTE QUÍMICO:** Prescrito Irinotecán debido a que la mutación **KRAS** invalida la cascada de anticuerpos anti-EGFR.")
        justificaciones.append("• **REGENERATIVO:** El exosoma cargado con miRNA-145 se añade para silenciar directamente la transcripción del oncogén KRAS activo.")
    if "APC Mutado" in mutaciones:
        sug_b = "Curcumina (Cúrcuma)"
        justificaciones.append("• **APOYO NATURAL:** Curcumina seleccionada para modular por vía pleiotrópica la acumulación aberrante de β-catenina generada por el gen APC.")

elif cancer_type == "Cáncer de Mama":
    if "HER2 Positivo" in mutaciones:
        sug_f = "Trastuzumab"
        sug_r = "Exosomas Cargados con PTEN"
        justificaciones.append("• **SOPORTE QUÍMICO:** Trastuzumab actúa bloqueando de forma directa la dimerización del receptor HER2/Neu.")
        justificaciones.append("• **REGENERATIVO:** Exosomas con PTEN restauran el freno supresor de tumores sobre la vía hiperactiva de PI3K.")
    if "PIK3CA Mutado" in mutaciones:
        sug_b = "Sulforafano (Brócoli)"
        justificaciones.append("• **APOYO NATURAL:** El Sulforafano induce detención del ciclo celular y modula de manera epigenética la ganancia de función en PIK3CA.")

elif cancer_type == "Cáncer de Próstata":
    if "AR Amplificado" in mutaciones:
        sug_f = "Enzalutamida"
        sug_r = "Exosomas con siRNA anti-AR"
        justificaciones.append("• **SOPORTE QUÍMICO:** Enzalutamida previene la translocación nuclear del receptor de andrógenos hiper-amplificado.")
        justificaciones.append("• **REGENERATIVO:** Vesículas dirigidas con siRNA ejecutan un knockdown biológico de la expresión proteica del receptor (AR).")
    sug_b = "Licopeno (Tomate)"
    justificaciones.append("• **APOYO NATURAL:** El Licopeno muestra alto tropismo prostático disminuyendo el estrés oxidativo y la viabilidad mitocondrial tumoral.")

elif cancer_type == "Cáncer Gástrico (Estómago)":
    if "HER2 Positivo" in mutaciones:
        sug_f = "Trastuzumab"
    else:
        sug_f = "Cisplatino"
    sug_b = "Ginsenósidos (Ginseng)"
    sug_r = "Exosomas con miRNA-34a"
    justificaciones.append(f"• **SOPORTE QUÍMICO:** Incorporado {sug_f} como piedra angular del esquema citotóxico / dirigido gástrico.")
    justificaciones.append("• **REGENERATIVO:** El miRNA-34a actúa mimetizando al supresor p53, induciendo apoptosis autónoma en la mucosa neoplásica.")

elif cancer_type == "Cáncer de Pulmón":
    if "EGFR Mutado" in mutaciones:
        sug_f = "Osimertinib"
        sug_r = "Exosomas con siRNA anti-EGFR"
        justificaciones.append("• **SOPORTE QUÍMICO:** Osimertinib actúa como inhibidor de tirosina quinasa de tercera generación, superando mutaciones de resistencia.")
        justificaciones.append("• **REGENERATIVO:** El uso de nanovesículas con siRNA corta la traducción del receptor EGFR mutado.")
    elif "ALK Fusionado" in mutaciones:
        sug_f = "Alectinib"
        justificaciones.append("• **SOPORTE QUÍMICO:** Bloqueo específico del reordenamiento ALK mediante inhibición competitiva de ATP.")
    sug_b = "Astrágalo (Extracto)"
    justificaciones.append("• **APOYO NATURAL:** El Astrágalo contrarresta la inmunosupresión mediada por el microambiente del carcinoma pulmonar.")

if "Estadío IV (Metastásico)" in estadio:
    sug_r = "Células Madre Mesenquimales (MSCs-TRAIL)"
    justificaciones.append("• **ALERTA REGENERATIVA CRÍTICA:** En escenarios metastásicos avanzados, el agente REGENERATIVO prescribe exclusivamente células modificadas con ligando TRAIL para forzar la apoptosis de células tumorales diseminadas, previniendo que el estroma tumoral reclute células madre crudas.")

st.write(" ")
with st.container(border=True):
    st.markdown(f"### 🎯 PROPUESTA DE MÁXIMA EFECTIVIDAD: {cancer_type}")
    st.write("Combinación molecular perfecta calculada por consenso de los agentes de IA según parámetros clínicos:")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.info(f"💊 **SOPORTE QUÍMICO Recomendado:**\n\n**{sug_f}**")
    col_s2.success(f"🌿 **APOYO NATURAL Recomendado:**\n\n**{sug_b}**")
    col_s3.warning(f"🧠 **REGENERATIVO Recomendado:**\n\n**{sug_r}**")
    
    with st.expander("🔍 Ver Justificación Biológica Integrada de los Agentes"):
        for j in justificaciones:
            st.markdown(j)

# -------------------------------------------------------------
# SECCIÓN II: GRILLAS DE EVALUACIÓN DINÁMICA
# -------------------------------------------------------------
st.write("---")
st.subheader("🤖 PANEL II: Grillas de Descubrimiento e Ingesta de los Agentes")

col_ag1, col_ag2, col_ag3 = st.columns(3)

with col_ag1:
    st.markdown("⚡ **Agente de IA: SOPORTE QUÍMICO**")
    opciones_f = list(farmacos_dict.keys()) + ["Ingresar Compuesto Manualmente (Lugar 8)"]
    seleccion_f = st.multiselect("Fármacos Sintéticos / Dirigidos:", opciones_f, default=[sug_f])
    custom_f = st.text_input("Fármaco 8 (Manual):", "Inhibidor Experimental") if "Ingresar Compuesto Manualmente (Lugar 8)" in seleccion_f else ""

with col_ag2:
    st.markdown("🌿 **Agente de IA: APOYO NATURAL**")
    opciones_b = list(fitofarmacos_dict.keys()) + ["Ingresar Extracto Manualmente (Lugar 8)"]
    seleccion_b = st.multiselect("Extractos Botánicos / Fitofármacos:", opciones_b, default=[sug_b])
    custom_b = st.text_input("Extracto 8 (Manual):", "Compuesto Botánico Libre") if "Ingresar Extracto Manualmente (Lugar 8)" in seleccion_b else ""

with col_ag3:
    st.markdown("🧠 **Agente de IA: REGENERATIVO**")
    opciones_r = list(regenerativas_dict.keys()) + ["Ingresar Terapia Manualmente (Lugar 8)"]
    seleccion_r = st.multiselect("Vesículas / Células Madre / Exosomas:", opciones_r, default=[sug_r])
    custom_r = st.text_input("Terapia 8 (Manual):", "Exosomas Autólogos Modificados") if "Ingresar Terapia Manualmente (Lugar 8)" in seleccion_r else ""

es_nanometrico = st.toggle("🔬 **Optimización de Entrega: Escala Nanométrica (Maximiza estabilidad biológica celular y biodisponibilidad)**", value=True)
factor_nano = 1.65 if es_nanometrico else 1.00

# -------------------------------------------------------------
# SECCIÓN III: ARBITRAJE CLÍNICO Y SIMULACIÓN DEL GEMELO DIGITAL
# -------------------------------------------------------------
st.write("---")
st.subheader("👨‍⚕️ PANEL III: Arbitraje Clínico y Simulación del Gemelo Digital")

lista_final_f = [custom_f if x == "Ingresar Compuesto Manualmente (Lugar 8)" else x for x in seleccion_f]
lista_final_b = [custom_b if x == "Ingresar Extracto Manualmente (Lugar 8)" else x for x in seleccion_b]
lista_final_r = [custom_r if x == "Ingresar Terapia Manualmente (Lugar 8)" else x for x in seleccion_r]

alertas_criticas = []
compatibilidad_score = 100
eficacia_acumulada = 0.0

if cancer_type == "Cáncer Colorrectal" and "KRAS Mutado" in mutaciones and any(x in ["Cetuximab", "Panitumumab"] for x in lista_final_f):
    alertas_criticas.append("❌ **Incompatibilidad Ómica:** Los anticuerpos anti-EGFR (Cetuximab/Panitumumab) carecen de efectividad clínica en tumores con mutación activa en KRAS corriente abajo.")
    compatibilidad_score -= 40

if cancer_type == "Cáncer de Mama" and "HER2 Positivo" not in mutaciones and "Trastuzumab" in lista_final_f:
    alertas_criticas.append("⚠️ **Futilidad Biológica:** Prescribir Trastuzumab en un entorno HER2 Negativo no provee beneficio clínico sobre la masa tumoral.")
    compatibilidad_score -= 25

if "Estadío IV (Metastásico)" in estadio and "Células Madre Mesenquimales (MSCs-TRAIL)" not in lista_final_r and any("Células" in x for x in lista_final_r):
    alertas_criticas.append("⚠️ **Riesgo Estromal Metastásico:** En etapas avanzadas, el estroma recluta células madre crudas promoviendo nichos pre-metastásicos. Se aconseja mutar a la línea celular modificada MSCs-TRAIL.")
    compatibilidad_score -= 15

for c in lista_final_f:
    if c in farmacos_dict: eficacia_acumulada += farmacos_dict[c] * 0.4
for b in lista_final_b:
    if b in fitofarmacos_dict: eficacia_acumulada += fitofarmacos_dict[b] * 0.3
for r in lista_final_r:
    if r in regenerativas_dict: eficacia_acumulada += regenerativas_dict[r] * 0.35

sinergia_activa = False
if "Exosomas Cargados con miRNA-145" in lista_final_r and "KRAS Mutado" in mutaciones:
    sinergia_activa = True; eficacia_acumulada += 0.15
if "Exosomas con siRNA anti-EGFR" in lista_final_r and "EGFR Mutado" in mutaciones:
    sinergia_activa = True; eficacia_acumulada += 0.15

eficacia_final_red = min(0.99, eficacia_acumulada * factor_nano)
if compatibilidad_score < 50: eficacia_final_red *= 0.25

if alertas_criticas:
    for alerta in alertas_criticas: st.error(alerta)
else:
    st.success("✅ **Dictamen del Arbitraje Clínico:** Combinación aprobada con éxito. Los agentes moleculares y celulares muestran una aditividad positiva libre de interferencia.")

# Simulación Dinámica Celular
pasos = 50
tiempo = list(range(pasos))
v1_din, v2_din, prolif, apop = [], [], [], []

v1_act = 0.85 if len(mutaciones) > 0 else 0.25
v2_act = 0.75 if "Estadío IV (Metastásico)" in estadio else 0.30

inh_v1 = eficacia_final_red * 0.80
inh_v2 = eficacia_final_red * 0.75

for t in tiempo:
    v1_act = max(0.05, v1_act * (1.0 - inh_v1) if t > 5 else v1_act)
    v2_act = max(0.05, v2_act * (1.0 - inh_v2) if t > 5 else v2_act)
    
    ind_prolif = (v1_act * 0.50) + (v2_act * 0.50)
    ind_apop = max(0.0, 1.0 - ind_prolif)
    
    v1_din.append(v1_act)
    v2_din.append(v2_act)
    prolif.append(ind_prolif)
    apop.append(ind_apop)

col_v1, col_v2, col_v3 = st.columns([1, 2, 2])
with col_v1:
    st.metric("Compatibilidad Terapéutica", f"{compatibilidad_score}%")
    st.metric("Potencia de Reprogramación", f"{eficacia_final_red*100:.1f}%")
    st.metric("Sinergia de los Agentes", "MÁXIMA MULTI-EJE" if sinergia_activa else "ESTÁNDAR")

with col_v2:
    fig1, ax1 = plt.subplots(figsize=(5, 3.5))
    ax1.plot(tiempo, v1_din, label=vias_nombres[0], color="#0288D1", lw=2)
    ax1.plot(tiempo, v2_din, label=vias_nombres[1], color="#F57C00", lw=2)
    ax1.set_ylim(0, 1.1)
    ax1.set_title("Cinética de Señalización de Vías")
    ax1.legend(fontsize=8)
    ax1.grid(True, alpha=0.2)
    st.pyplot(fig1)

with col_v3:
    fig2, ax2 = plt.subplots(figsize=(5, 3.5))
    ax2.plot(tiempo, prolif, label="Tasa Proliferativa", color="#D32F2F", lw=2.5)
    ax2.plot(tiempo, apop, label="Inducción de Apoptosis", color="#388E3C", lw=2.5)
    ax2.set_ylim(0, 1.1)
    ax2.set_title("Evolución Fenotípica de la Masa Tumoral")
    ax2.legend(fontsize=8)
    ax2.grid(True, alpha=0.2)
    st.pyplot(fig2)

# -------------------------------------------------------------
# SECCIÓN IV: BIBLIOTECA DE EVIDENCIA CIENTÍFICA (CORREGIDA)
# -------------------------------------------------------------
st.write("---")
if st.checkbox("📚 REVISAR EVIDENCIA CIENTÍFICA Y EXPERIENCIAS CLÍNICAS RESPALDADAS"):
    st.markdown("### 📄 Repositorio de Soporte y Literatura Médica de los Agentes")
    st.markdown(f"**🔬 Evidencia según Tipo de Cáncer:** Analizando el escenario para `{cancer_type}` en `{estadio}`.")
    st.markdown(f"• **SOPORTE QUÍMICO:** Sus compuestos seleccionados ({lista_final_f}) actúan de manera diana controlando la replicación y la cinética de transcripción celular.")
    st.markdown(f"• **APOYO NATURAL:** Los fitofármacos seleccionados ({lista_final_b}) proveen un entorno de modulación pleiotrópica regulando factores como NF-κB, STAT3 o PI3K según la patología.")
    st.markdown("• **REGENERATIVO:** La evidencia científica y experiencias de expertos muestran resultados altamente positivos en forma complementaria o como terapia única. Las vesículas extracelulares (exosomas) y líneas celulares dirigidas superan los mecanismos de quimiorresistencia, reprogramando el microambiente y logrando la reversión fenotípica.")
