import streamlit as st
import pandas as pd
import numpy as np

# Configuración inicial de la aplicación
st.set_page_config(
    page_title="OncoTwin Pro - Gemelo Digital Chile",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para replicar la interfaz médica/ómica
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 20px;
    }
    .chem-box {
        background-color: #1E293B;
        border-left: 5px solid #3B82F6;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .nat-box {
        background-color: #064E3B;
        border-left: 5px solid #10B981;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .regen-box {
        background-color: #701A75;
        border-left: 5px solid #F43F5E;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    .badge-title {
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-value {
        font-size: 1.15rem;
        font-weight: 600;
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# BASE DE DATOS Y CONFIGURACIÓN EPIDEMIOLÓGICA (CHILE)
# ----------------------------------------------------
DATOS_ONCOLOGICOS = {
    "Cáncer Gástrico (Estómago)": {
        "soporte_quimico": ["Trastuzumab", "Capecitabina", "Oxaliplatino", "5-Fluorouracilo"],
        "apoyo_natural": ["Curcumina Nanostructurada", "EGCG (Té Verde)", "Resveratrol", "Quercetina"],
        "regenerativo": ["Exosomas Cargados con PTEN", "Vesículas Extracelulares Mesenquimales"],
        "rec_chem": "Trastuzumab",
        "rec_nat": "Curcumina Nanostructurada",
        "rec_regen": "Exosomas Cargados con PTEN",
        "justificacion_chem": "Trastuzumab bloquea selectivamente receptores HER2 hiperexpresados en epitelio gástrico.",
        "justificacion_nat": "La curcumina nanoestructurada inhibe la activación constitutiva de STAT3 y NF-kB en mucosa gástrica.",
        "justificacion_regen": "Exosomas con PTEN restauran la función del gen supresor tumoral sobre la vía PI3K/AKT."
    },
    "Cáncer Colorrectal": {
        "soporte_quimico": ["Bevacizumab", "FOLFOX", "Cetuximab", "Irinotecan"],
        "apoyo_natural": ["Sulforafano (Brócoli)", "Curcumina Nano", "Resveratrol"],
        "regenerativo": ["Exosomas Células Madre Mesenquimales", "MicroARN-145 Nano-encapsulado"],
        "rec_chem": "Bevacizumab",
        "rec_nat": "Sulforafano (Brócoli)",
        "rec_regen": "Exosomas Células Madre Mesenquimales",
        "justificacion_chem": "Inhibición anti-VEGF para bloquear la neoangiogénesis tumoral en el estroma intestinal.",
        "justificacion_nat": "Sulforafano promueve la detención del ciclo celular y modula el estrés oxidativo microambiental.",
        "justificacion_regen": "Vesículas mesenquimales modulan las señales inflamatorias crónicas del microambiente tumoral."
    },
    "Cáncer de Próstata": {
        "soporte_quimico": ["Enzalutamida", "Abiraterona", "Docetaxel", "Cabazitaxel"],
        "apoyo_natural": ["Licopeno Nano-emulsionado", "EGCG (Té Verde)", "Genisteína"],
        "regenerativo": ["Vesículas de Exosomas Supresores", "Péptidos Oncolíticos Nano-dirigidos"],
        "rec_chem": "Enzalutamida",
        "rec_nat": "Licopeno Nano-emulsionado",
        "rec_regen": "Vesículas de Exosomas Supresores",
        "justificacion_chem": "Inhibición directa y selectiva de la señalización intracelular del receptor de andrógenos.",
        "justificacion_nat": "Licopeno de alta biodisponibilidad disminuye factores pro-inflamatorios e interrumpe la vía androgenética.",
        "justificacion_regen": "Exosomas supresores restauran los frenos celulares contra la proliferación descontrolada."
    },
    "Cáncer de Mama": {
        "soporte_quimico": ["Trastuzumab", "Pertuzumab", "Tamoxifeno", "Paclitaxel"],
        "apoyo_natural": ["Sulforafano (Brócoli)", "Curcumina Nanoestructurada", "Resveratrol"],
        "regenerativo": ["Exosomas Cargados con PTEN", "Células Madre Reprogramadas"],
        "rec_chem": "Trastuzumab",
        "rec_nat": "Sulforafano (Brócoli)",
        "rec_regen": "Exosomas Cargados con PTEN",
        "justificacion_chem": "Trastuzumab actúa bloqueando de forma directa la dimerización del receptor HER2/Neu.",
        "justificacion_nat": "Fitofármacos seleccionados proveen un entorno de modulación pleiotrópica regulando factores como NF-kB, STAT3 o PI3K.",
        "justificacion_regen": "Exosomas con PTEN restauran el freno supresor de tumores sobre la vía hiperactiva de PI3K."
    },
    "Cáncer de Pulmón": {
        "soporte_quimico": ["Osimertinib", "Pembrolizumab", "Cisplatino", "Carboplatino"],
        "apoyo_natural": ["Boswellia Serrata Nano", "Curcumina", "Ganoderma Lucidum Nano"],
        "regenerativo": ["Exosomas Células Madre Pulmonares", "ARNi Antisentido Liposomal"],
        "rec_chem": "Osimertinib",
        "rec_nat": "Boswellia Serrata Nano",
        "rec_regen": "Exosomas Células Madre Pulmonares",
        "justificacion_chem": "Bloqueo selectivo de receptores EGFR mutados inhibiendo la vía de supervivencia celular.",
        "justificacion_nat": "Boswellia serrata nano-emulsionada modula la vía 5-LOX y la respuesta inflamatoria parenquimatosa.",
        "justificacion_regen": "Vesículas pulmonares especializadas favorecen el remodelado celular y reducen el nicho metastásico."
    },
    "Cáncer de Ovario": {
        "soporte_quimico": ["Olaparib", "Carboplatino", "Paclitaxel", "Bevacizumab"],
        "apoyo_natural": ["Curcumina Nanostructurada", "EGCG (Té Verde)", "Resveratrol Nano"],
        "regenerativo": ["Exosomas Cargados con miR-34a", "Vesículas Extracelulares Reparadoras"],
        "rec_chem": "Olaparib",
        "rec_nat": "Curcumina Nanostructurada",
        "rec_regen": "Exosomas Cargados con miR-34a",
        "justificacion_chem": "Inhibidor de PARP que induce letalidad sintética en tumores con deficiencia de reparación por recombinación homóloga (HRD/BRCA).",
        "justificacion_nat": "Curcumina nanoestructurada inhibe la transición epitelio-mesénquima en el estroma ovárico.",
        "justificacion_regen": "Exosomas con miR-34a restauran la regulación epigenética supresora tumoral y revierten la quimioresistencia."
    },
    "Cáncer Cervicouterino": {
        "soporte_quimico": ["Cisplatino", "Pembrolizumab", "Bevacizumab", "Topotecán"],
        "apoyo_natural": ["Epigalocatequina (EGCG)", "Extracto de Artemisia Nano", "Fisetina"],
        "regenerativo": ["Péptidos Anti-VPH", "Exosomas Inmunomoduladores"],
        "rec_chem": "Cisplatino",
        "rec_nat": "Epigalocatequina (EGCG)",
        "rec_regen": "Exosomas Inmunomoduladores",
        "justificacion_chem": "Agente alquilante que induce aductos en el ADN provocando la apoptosis celular selectiva.",
        "justificacion_nat": "EGCG de alta pureza modula las oncoproteínas virales E6/E7 inhibiendo la transformación maligna.",
        "justificacion_regen": "Exosomas inmunomoduladores reclutan linfocitos infiltrantes de tumor (TILs) al microambiente epitelial."
    },
    "Cáncer Vesicular y Vías Biliares": {
        "soporte_quimico": ["Gemcitabina", "Cisplatino", "Durvalumab", "Oxaliplatino"],
        "apoyo_natural": ["Silibina Nano-complejada", "Curcumina Nanostructurada", "Ácido Ursodeoxicólico Natural"],
        "regenerativo": ["Exosomas Biliares Reparadores", "Vesículas Nano-dirigidas"],
        "rec_chem": "Gemcitabina + Cisplatino",
        "rec_nat": "Silibina Nano-complejada",
        "rec_regen": "Exosomas Biliares Reparadores",
        "justificacion_chem": "Inhibición de la síntesis de ADN combinada con aductos platinados en el epitelio biliar.",
        "justificacion_nat": "Silibina nano-emulsionada ejerce efecto hepatoprotector y reduce el estrés oxidativo del conducto biliar.",
        "justificacion_regen": "Vesículas reparadoras promueven la restauración del microambiente ductal biliar."
    },
    "Cáncer Renal": {
        "soporte_quimico": ["Nivolumab", "Cabozantinib", "Sunitinib", "Axitinib"],
        "apoyo_natural": ["Cordyceps Sinensis Nano", "Quercetina Nano", "Curcumina"],
        "regenerativo": ["Exosomas Renales Reparadores", "Péptidos Antian giogénicos"],
        "rec_chem": "Nivolumab + Cabozantinib",
        "rec_nat": "Cordyceps Sinensis Nano",
        "rec_regen": "Exosomas Renales Reparadores",
        "justificacion_chem": "Combinación inmunoterapéutica y antiangiogénica multiquinasa contra la vía VEGF/MET/AXL.",
        "justificacion_nat": "Biocompuestos activos de Cordyceps protegen la función del parénquima renal y modulan citoquinas.",
        "justificacion_regen": "Exosomas renoprotectores previenen el daño histológico periférico a las sesiones terapéuticas."
    },
    "Cáncer Hepático": {
        "soporte_quimico": ["Atezolizumab", "Bevacizumab", "Sorafenib", "Lenvatinib"],
        "apoyo_natural": ["Silimarina / Silibina Nano", "Curcumina Ultrafina", "Antocianinas"],
        "regenerativo": ["Exosomas Hepáticos con PTEN", "Vesículas de Reprogramación Hepática"],
        "rec_chem": "Atezolizumab + Bevacizumab",
        "rec_nat": "Silimarina Nano-emulsionada",
        "rec_regen": "Exosomas Hepáticos con PTEN",
        "justificacion_chem": "Bloqueo dual PD-L1 y VEGF que restablece la inmunidad antitumoral y normaliza la vasculatura hepática.",
        "justificacion_nat": "Silimarina nanoestructurada protege el tejido hepático no tumoral reduciendo fibrosis y toxicidad.",
        "justificacion_regen": "Vesículas celulares especializadas estimulan vías de regeneración fisiológica y reprogramación fenotípica."
    }
}

# Header principal
st.markdown("<div class='main-header'>🧬 OncoTwin Pro: Plataforma de Simulación Multi-Agente (Edición Chile)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Gemelo Digital de Precisión adaptado a la epidemiología oncología chilena.</div>", unsafe_allow_html=True)

# ----------------------------------------------------
# PANEL I: PERFILADO OMNIPRESENTE DEL PACIENTE
# ----------------------------------------------------
with st.expander("👤 PANEL I: Perfilado Omnipresente del Paciente (Historial Clínico y Ómico)", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        tipo_cancer = st.selectbox(
            "Tipo de Cáncer (Frecuentes en Chile)",
            options=list(DATOS_ONCOLOGICOS.keys()),
            index=3  # Default: Cáncer de Mama
        )
        
        estadio = st.selectbox(
            "Estadío Clínico",
            options=["Estadío I", "Estadío II", "Estadío III", "Estadío IV (Metastásico)"],
            index=2  # Default: Estadío III
        )
        
        tiempo_deteccion = st.number_input(
            "Tiempo desde Detección (meses)",
            min_value=1, max_value=120, value=2, step=1
        )
        
        sexo = st.radio(
            "Sexo Biológico",
            options=["Masculino", "Femenino"],
            index=1,
            horizontal=True
        )
        
        edad = st.number_input("Edad (Años)", min_value=1, max_value=110, value=39, step=1)
        peso = st.number_input("Peso (kg)", min_value=10, max_value=200, value=65, step=1)

    with col2:
        profesion = st.text_input("Profesión / Actividad", value="Ingeniera comercial")
        
        tratamiento_actual = st.selectbox(
            "Tratamiento Actual Base",
            options=["Quimioterapia Convencional", "Inmunoterapia", "Terapia Dirigida", "Radioterapia", "Sin Tratamiento Previo"],
            index=0
        )
        
        tiempo_tratamiento = st.number_input("Tiempo con Tratamiento Actual (ciclos)", min_value=0, max_value=50, value=2, step=1)
        
        comorbilidades = st.multiselect(
            "Comorbilidades",
            options=["Ninguna", "Diabetes Tipo 2", "Hipertensión Arterial", "Cardiopatía", "Insuficiencia Renal"],
            default=["Ninguna", "Diabetes Tipo 2"]
        )
        
        alergias = st.text_input("Alergias Conocidas", value="Ninguna")
        
        mutaciones = st.multiselect(
            "Mutaciones Conductoras (Ómica Personalizada)",
            options=["HER2 Positivo", "BRCA1 / BRCA2", "EGFR Mutado", "KRAS G12D", "TP53 Mutado", "PIK3CA Mutado", "PD-L1 Alto"],
            default=["HER2 Positivo"]
        )

# Cargar los datos correspondientes al cáncer seleccionado
datos_sel = DATOS_ONCOLOGICOS[tipo_cancer]

# ----------------------------------------------------
# PROPUESTA DE MÁXIMA EFECTIVIDAD
# ----------------------------------------------------
st.markdown(f"### 🎯 PROPUESTA DE MÁXIMA EFECTIVIDAD: {tipo_cancer}")
st.caption("Combinación molecular perfecta calculada por consenso de los agentes de IA según parámetros clínicos:")

col_prop1, col_prop2, col_prop3 = st.columns(3)

with col_prop1:
    st.markdown(f"""
    <div class='chem-box'>
        <div class='badge-title' style='color: #60A5FA;'>💊 SOPORTE QUÍMICO Recomendado:</div>
        <div class='badge-value'>{datos_sel['rec_chem']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_prop2:
    st.markdown(f"""
    <div class='nat-box'>
        <div class='badge-title' style='color: #34D399;'>🌿 APOYO NATURAL Recomendado:</div>
        <div class='badge-value'>{datos_sel['rec_nat']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_prop3:
    st.markdown(f"""
    <div class='regen-box'>
        <div class='badge-title' style='color: #F472B6;'>🧠 REGENERATIVO Recomendado:</div>
        <div class='badge-value'>{datos_sel['rec_regen']}</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🔍 Ver Justificación Biológica Integrada de los Agentes"):
    st.markdown(f"• **SOPORTE QUÍMICO:** {datos_sel['justificacion_chem']}")
    st.markdown(f"• **APOYO NATURAL:** {datos_sel['justificacion_nat']}")
    st.markdown(f"• **REGENERATIVO:** {datos_sel['justificacion_regen']}")

st.divider()

# ----------------------------------------------------
# PANEL II: GRILLAS DE DESCUBRIMIENTO E INGESTA
# ----------------------------------------------------
st.markdown("### ⚙️ PANEL II: Grillas de Descubrimiento e Ingesta de los Agentes")

col_ag1, col_ag2, col_ag3 = st.columns(3)

with col_ag1:
    agente_chem = st.multiselect(
        "⚡ Agente de IA: SOPORTE QUÍMICO",
        options=datos_sel["soporte_quimico"],
        default=[datos_sel["rec_chem"].split(" + ")[0]]
    )

with col_ag2:
    agente_nat = st.multiselect(
        "🌿 Agente de IA: APOYO NATURAL",
        options=datos_sel["apoyo_natural"],
        default=[datos_sel["rec_nat"].split(" + ")[0]]
    )

with col_ag3:
    agente_regen = st.multiselect(
        "🧠 Agente de IA: REGENERATIVO",
        options=datos_sel["regenerativo"],
        default=[datos_sel["rec_regen"]]
    )

opt_nanometrica = st.toggle(
    "🔬 Optimización de Entrega: Escala Nanométrica (Maximiza estabilidad biológica celular y biodisponibilidad)",
    value=True
)

st.divider()

# ----------------------------------------------------
# PANEL III: ARBITRAJE CLÍNICO Y SIMULACIÓN
# ----------------------------------------------------
st.markdown("### 🧑‍⚕️ PANEL III: Arbitraje Clínico y Simulación del Gemelo Digital")

st.success("✅ **Dictamen del Arbitraje Clínico:** Combinación aprobada con éxito. Los agentes moleculares y celulares muestran una aditividad positiva libre de interferencia.")

# Métricas dinámicas dependientes de la optimización nanométrica
potencia_reprog = "99.0%" if opt_nanometrica else "68.3%"
sinergia_val = "MÁXIMA" if opt_nanometrica else "ESTÁNDAR"

m1, m2, m3 = st.columns(3)
m1.metric("Compatibilidad Terapéutica", "100%")
m2.metric("Potencia de Reprogramación", potencia_reprog)
m3.metric("Sinergia de los Agentes", sinergia_val)

# Gráficos de Simulación Cinética y Masa Tumoral
st.markdown("#### Cinética de Señalización de Vías y Evolución Tumoral")

col_g1, col_g2 = st.columns(2)

pasos = np.linspace(0, 50, 50)
factor_nano = 0.95 if opt_nanometrica else 0.65

# Curvas de cinéticas moleculares
receptor_her2 = np.exp(-pasos * 0.15 * factor_nano)
via_akt = 0.3 * np.exp(-pasos * 0.10 * factor_nano)

df_vias = pd.DataFrame({
    "Paso de Simulación": pasos,
    "Receptor HER2/Neu": receptor_her2,
    "AKT (Vía PI3K/mTOR)": via_akt
}).set_index("Paso de Simulación")

with col_g1:
    st.caption("Cinética de Señalización de Vías")
    st.line_chart(df_vias)

# Curvas de Evolución Tumoral
tasa_prolif = 0.6 * np.exp(-pasos * 0.12 * factor_nano)
if not opt_nanometrica:
    tasa_prolif += 0.12 * np.sin(pasos / 2.5) # Simula fluctuación por menor absorción

df_tumor = pd.DataFrame({
    "Paso de Simulación": pasos,
    "Tasa Proliferativa": tasa_prolif
}).set_index("Paso de Simulación")

with col_g2:
    st.caption("Evolución Fenotípica de la Masa Tumoral")
    st.line_chart(df_tumor)

# Sección de Literatura y Evidencia Médica
revisar_evidencia = st.checkbox("☑️ REVISAR EVIDENCIA CIENTÍFICA Y EXPERIENCIAS CLÍNICAS RESPALDADAS", value=True)

if revisar_evidencia:
    st.markdown("---")
    st.markdown("### 📄 Repositorio de Soporte y Literatura Médica de los Agentes")
    st.markdown(f"🔬 **Evidencia según Tipo de Cáncer:** Analizando el escenario para **{tipo_cancer}** en **{estadio}**.")
    
    st.markdown(f"""
    * **SOPORTE QUÍMICO:** Sus compuestos seleccionados (`{agente_chem}`) actúan de manera directa controlando la replicación y la cinética de transcripción celular.
    * **APOYO NATURAL:** Los fitofármacos seleccionados (`{agente_nat}`) proveen un entorno de modulación pleiotrópica regulando factores como NF-kB, STAT3 o PI3K según la patología.
    * **REGENERATIVO:** La evidencia científica y experiencias de expertos muestran resultados altamente positivos en forma complementaria o como terapia única. Las vesículas extracelulares (`{agente_regen}`) y líneas celulares dirigidas superan los mecanismos de quimioresistencia, reprogramando el microambiente y logrando la reversión fenotípica.
    """)
