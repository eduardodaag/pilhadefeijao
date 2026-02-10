import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="Pilha de Feijão", page_icon="🫘", layout="wide")

st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
        gap: 5px;
        padding: 10px;
    }
    .number-box {
        padding: 10px 0;
        text-align: center;
        border-radius: 5px;
        font-weight: bold;
        font-size: 11px;
        color: white;
    }
    .occupied { background-color: #FF4B4B; }
    .available { background-color: #28a745; }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Pilha de Feijão: 0 a 30.000")

try:
    # Cache buster para garantir atualização em tempo real
    df = pd.read_csv(f'palpites.csv?cache={time.time()}')
    numeros_ocupados = set(df['palpite'].tolist())

    st.subheader("🔍 Verificar meu número")
    # Busca ajustada para 0 a 30.000
    busca = st.number_input("Número desejado:", 0, 30000, 0)
    
    if busca in numeros_ocupados:
        dono = df[df['palpite'] == busca]['usuario'].values[0]
        st.error(f"❌ O número {busca} já é do @{dono}")
    else:
        st.success(f"✅ O número {busca} está LIVRE!")

    st.divider()

    st.subheader("🗺️ Mapa de Números (0 a 30.000)")
    # Slider ajustado para o novo limite
    inicio = st.slider("Visualizar a partir de:", 0, 30000, 0, step=500)
    fim = min(inicio + 499, 30000)

    st.info(f"Mostrando números de **{inicio}** até **{fim}**")

    grid_html = '<div class="grid-container">'
    for i in range(inicio, fim + 1):
        status = "occupied" if i in numeros_ocupados else "available"
        grid_html += f'<div class="number-box {status}">{i}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

except:
    st.warning("Aguardando sincronização de dados...")