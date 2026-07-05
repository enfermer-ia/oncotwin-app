import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la interfaz de usuario
st.set_page_config(page_title="OncoTwin - Gemelo Digital", layout="wide")
st.title("🧬 OncoTwin: Simulación de Reprogramación de Vías Moleculares")
st.write("Plataforma predictiva para evaluar la inversión de señales celulares en cáncer colorrectal.")

# -------------------------------------------------------------
# PARÁMETROS DE ENTRADA: CONFIGURACIÓN DE VARIABLES DE LA RED
# -------------------------------------------------------------
st.sidebar.header("🎛️ Estado Genético del Paciente")
apc_mutado = st.sidebar.checkbox("Mutación en APC (Falla Complejo Degradación)", value=True)
kras_mutado = st.sidebar.checkbox("Mutación en KRAS (Señal MAPK Activa)", value=True)

st.sidebar.header("🧪 Configuración del Tratamiento")

# REQUERIMIENTO: Selección del tipo de producto base
tipo_producto = st.sidebar.radio("Selecciona el producto a someter a simulación:", ["Fármaco Sintético", "Extracto Botánico"])

# Selección específica y asignación de potencias biológicas basales
if tipo_producto == "Fármaco Sintético":
    producto = st.sidebar.selectbox("Seleccionar Fármaco", ["5-Fluorouracilo (5-FU)", "Regorafenib", "Cetuximab"])
    potencia_base = 0.55
else:
    producto = st.sidebar.selectbox("Seleccionar Extracto Botánico", ["Curcumina (Cúrcuma)", "Quercetina (Fitoquímico)", "Epigalocatequina (Té Verde)"])
    potencia_base = 0.35

# REQUERIMIENTO: Factor nanométrico
es_nanometrico = st.sidebar.toggle("¿Utilizar formulación nanométrica? (Nano-delivery)", value=True)

# El tamaño nanométrico amplifica programáticamente la eficacia en la ecuación
if es_nanometrico:
    factor_nano = 1.6  # Incremento del 60% en penetración celular
    st.sidebar.caption("✨ **Modo Nano Activado:** Modelando liberación celular optimizada a escala de 50-200nm.")
else:
    factor_nano = 1.0
    st.sidebar.caption("⚠️ **Modo Estándar:** Formulación libre convencional con tasas de aclaramiento normales.")

dosis = st.sidebar.slider("Concentración / Dosis Administrada", 0.1, 2.0, 1.0, 0.1)
pasos_tiempo = st.sidebar.slider("Horizonte de Simulación (Ciclos Celulares)", 10, 100, 50, 5)

# Cálculo de la inhibición efectiva combinando dosis, potencia y el vector nanométrico
potencia_efectiva = min(0.95, potencia_base * dosis * factor_nano)

# Simulación de la afinidad: Los extractos son multiobjetivo; los fármacos son más específicos
if tipo_producto == "Extracto Botánico":
    inhibicion_wnt = potencia_efectiva * 0.9
    inhibicion_mapk = potencia_efectiva * 0.8
else:
    if producto == "5-Fluorouracilo (5-FU)":
        inhibicion_wnt = potencia_efectiva * 0.3
        inhibicion_mapk = potencia_efectiva * 0.9
    else:
        inhibicion_wnt = potencia_efectiva * 0.1
        inhibicion_mapk = potencia_efectiva * 0.95

# -------------------------------------------------------------
# NÚCLEO DE SIMULACIÓN (CÓDIGO CORREGIDO SIN ERRORES DE SINTAXIS)
# -------------------------------------------------------------
def ejecutar_simulacion_red(apc, kras, inh_wnt, inh_mapk, pasos):
    tiempo = list(range(pasos))
    beta_catenin = []
    erk_active = []
    proliferacion = []
    apoptosis = []
    
    b_cat_actual = 0.8 if apc else 0.2
    erk_actual = 0.9 if kras else 0.1
    
    for t in tiempo:
        if apc:
            b_cat_actual = 0.9 * (1.0 - inh_wnt)
        else:
            b_cat_actual = max(0.1, 0.2 * (1.0 - inh_wnt))
            
        if kras:
            erk_actual = 0.95 * (1.0 - inh_mapk)
        else:
            erk_actual = max(0.05, 0.15 * (1.0 - inh_mapk))
            
        ind_prolif = (b_cat_actual * 0.6) + (erk_actual * 0.4)
        ind_apop = max(0.0, 1.0 - ind_prolif)
        
        beta_catenin.append(b_cat_actual)
        erk_active.append(erk_actual)
        proliferacion.append(ind_prolif)
        apoptosis.append(ind_apop)
        
    return tiempo, beta_catenin, erk_active, proliferacion, apoptosis

# Mapeo explícito y seguro de variables de entrada
t, b_cat, erk, prolif, apop = ejecutar_simulacion_red(
    apc=apc_mutado, 
    kras=kras_mutado, 
    inh_wnt=inhibicion_wnt, 
    inh_mapk=inhibicion_mapk, 
    pasos=pasos_tiempo
)

# -------------------------------------------------------------
# INTERFAZ DE USUARIO: REPORTES DEL GEMELO DIGITAL
# -------------------------------------------------------------
st.subheader(f"📊 Resultados de Evaluación: {producto} ({'Formulación Nano' if es_nanometrico else 'Formulación Estándar'})")

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Inhibición Molecular Total", f"{potencia_efectiva*100:.1f}%")
with col_m2:
    st.metric("Índice de Proliferación Final", f"{prolif[-1]*100:.1f}%")
with col_m3:
    st.metric("Tasa de Apoptosis (Inversión)", f"{apop[-1]*100:.1f}%")

col1, col2 = st.columns(2)
with col1:
    st.write("### 📉 Mitigación de Expresión en Vías de Señalización")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(t, b_cat, label="β-catenina (Vía Wnt)", color="#0288D1", linewidth=2.5)
    ax1.plot(t, erk, label="ERK Activa (Vía MAPK)", color="#F57C00", linewidth=2.5)
    ax1.set_ylim(0, 1.1)
    ax1.set_ylabel("Nivel de Señal de la Proteína")
    ax1.set_xlabel("Ciclos de Simulación")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    st.pyplot(fig1)

with col2:
    st.write("### 🎯 Reprogramación del Destino Tumoral (Fenotipo)")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(t, prolif, label="Frenado de Proliferación", color="#D32F2F", linewidth=2.5)
    ax2.plot(t, apop, label="Inducción a la Apoptosis", color="#388E3C", linewidth=2.5)
    ax2.set_ylim(0, 1.1)
    ax2.set_ylabel("Índice de Actividad Celular")
    ax2.set_xlabel("Ciclos de Simulación")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    st.pyplot(fig2)
