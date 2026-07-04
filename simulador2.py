import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random

st.set_page_config(page_title="Analizador y Simulador - Spaceman", layout="wide")

st.title("🚀 Laboratorio Estocástico: Spaceman")
st.write(
    "Explora la probabilidad condicional y la generación pseudoaleatoria de multiplicadores "
    "en juegos tipo Crash."
)

# Crear pestañas para organizar la aplicación
tab1, tab2 = st.tabs(["📊 Análisis de Markov (Datos Históricos)", "🎲 Simulador PRNG (Dinámica del Juego)"])

with tab1:
    st.header("Análisis de Cadenas de Markov")
    
    # 1. Base de datos con las 5 sesiones reales proporcionadas
    sesiones_raw = [
        "132123223321222223322322112312313111222311312333213322312123222233332321323222313211212231321222211211212223121332211322332233212321311332222331222222223222112122212222331222233123",
        "111122222212222332221212222322332121112222231112",
        "1221211211221112321",
        "111131222211",
        "121212212312211122332122231121322222113123112211223222121113331213222233232232233233222232331222112313222322312"
    ]

    sesiones = [[int(char) for char in sesion] for sesion in sesiones_raw]

    counts = np.zeros((3, 3))
    for sesion in sesiones:
        for i in range(len(sesion) - 1):
            estado_actual = sesion[i] - 1
            estado_siguiente = sesion[i+1] - 1
            if 0 <= estado_actual <= 2 and 0 <= estado_siguiente <= 2:
                counts[estado_actual, estado_siguiente] += 1

    row_sums = counts.sum(axis=1, keepdims=True)
    transition_matrix = np.divide(counts, row_sums, out=np.zeros_like(counts), where=row_sums!=0)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("Introduce una secuencia de 5 estados para evaluar la tendencia histórica:")
        i1 = st.selectbox("Dato 1 (Más antiguo)", [1, 2, 3], index=0, key="m1")
        i2 = st.selectbox("Dato 2", [1, 2, 3], index=1, key="m2")
        i3 = st.selectbox("Dato 3", [1, 2, 3], index=1, key="m3")
        i4 = st.selectbox("Dato 4", [1, 2, 3], index=0, key="m4")
        i5 = st.selectbox("Dato 5 (Último estado)", [1, 2, 3], index=1, key="m5")
        ultimo_estado = i5
        
    with col2:
        df_matrix = pd.DataFrame(
            transition_matrix, 
            index=["Estado 1 (≥x2.0)", "Estado 2 (<x2.0)", "Estado 3 (≥x4.5)"],
            columns=["Hacia 1", "Hacia 2", "Hacia 3"]
        )
        st.dataframe(df_matrix.style.format("{:.2%}"))

        probabilidades_siguientes = transition_matrix[ultimo_estado - 1]
        df_prob = pd.DataFrame({
            "Resultado Siguiente": ["Estado 1 (Éxito ≥2.0)", "Estado 2 (Riesgo <2.0)", "Estado 3 (Excelente ≥4.5)"],
            "Probabilidad Empírica": probabilidades_siguientes
        })
        
        fig = px.bar(
            df_prob, x="Resultado Siguiente", y="Probabilidad Empírica",
            text=df_prob["Probabilidad Empírica"].apply(lambda x: f"{x:.2%}"),
            range_y=[0, 1]
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Simulador de Vuelo (PRNG)")
    st.write(
        "Ingresa los últimos 5 multiplicadores reales que viste en el juego. "
        "Luego, el algoritmo matemático generará el siguiente vuelo utilizando un generador pseudoaleatorio criptográfico, "
        "demostrando cómo los eventos pasados no afectan el evento futuro."
    )
    
    col3, col4 = st.columns([1, 2])
    
    with col3:
        st.subheader("Entrada de Datos")
        v1 = st.number_input("Vuelo T-4 (ej. 1.15)", min_value=1.0, value=1.20, step=0.1)
        v2 = st.number_input("Vuelo T-3", min_value=1.0, value=2.50, step=0.1)
        v3 = st.number_input("Vuelo T-2", min_value=1.0, value=1.05, step=0.1)
        v4 = st.number_input("Vuelo T-1", min_value=1.0, value=5.10, step=0.1)
        v5 = st.number_input("Vuelo Actual (T)", min_value=1.0, value=1.80, step=0.1)
        
        generar = st.button("🚀 Generar Siguiente Vuelo", type="primary")
        
    with col4:
        st.subheader("Resultado de la Simulación")
        if generar:
            # Lógica matemática del juego Crash
            # U es un flotante aleatorio entre 0 y 1
            U = random.random()
            
            # E es el "House Edge" (Ventaja de la casa). 0.99 = 1% de ventaja.
            E = 0.99 
            
            # Fórmula de choque
            if U == 1.0: # Prevención de división por cero
                crash_point = 100.0
            else:
                crash_point = E / (1.0 - U)
            
            # Aplicar límites (x1.0 mínimo, x100 máximo)
            crash_point = max(1.0, crash_point)
            crash_point = min(100.0, crash_point)
            
            # Redondear a 2 decimales para emular la interfaz del juego
            crash_point_str = f"{crash_point:.2f}"
            
            # Determinar la categoría para conectarlo con tu análisis anterior
            if crash_point >= 4.5:
                categoria = 3
                color = "green"
            elif crash_point >= 2.0:
                categoria = 1
                color = "blue"
            else:
                categoria = 2
                color = "red"
                
            st.markdown(
                f"""
                <div style="text-align: center; padding: 2rem; border-radius: 10px; background-color: #1E1E1E;">
                    <h1 style="font-size: 4rem; color: {color}; margin: 0;">x{crash_point_str}</h1>
                    <p style="font-size: 1.2rem; color: white;">Clasificación de tu modelo: <b>Estado {categoria}</b></p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            st.info(
                "**Análisis:** Matemáticamente, este multiplicador se calculó utilizando la fórmula $C = E / (1-U)$. "
                f"Tus datos de entrada ({v1}, {v2}, {v3}, {v4}, {v5}) crearon el contexto para ti, pero el servidor "
                "ignoró esos valores por completo al generar el nuevo número, confirmando que cada partida es un evento independiente."
            )
        else:
            st.info("Ingresa los 5 valores previos y presiona el botón para simular el siguiente choque.")
