import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# Configurações da Página
st.set_page_config(
    page_title="Groq Grid Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS para forçar o Tema Dark e Estilo Moderno
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
    }
    div[data-testid="stMetricValue"] {
        color: #818cf8;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #4f46e5;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DE CONEXÃO ---
# Substitua pelo IP da sua VPS
API_BASE_URL = "http://seu-ip-da-vps:8000"

st.title("⚡ GROQ GRID HUB")
st.subheader("AI-Driven Trading Control Panel")

# Sidebar para Configurações
st.sidebar.header("⚙️ Parâmetros da Grade")
upper_limit = st.sidebar.number_input("Limite Superior", value=70000)
lower_limit = st.sidebar.number_input("Limite Inferior", value=60000)
grid_count = st.sidebar.number_input("Número de Grades", value=30)

if st.sidebar.button("Salvar Configurações"):
    payload = {"upperLimit": upper_limit, "lowerLimit": lower_limit, "gridCount": grid_count}
    try:
        requests.post(f"{API_BASE_URL}/update-config", json=payload)
        st.sidebar.success("Configurações Atualizadas!")
    except:
        st.sidebar.error("Erro ao conectar na VPS")

# --- DASHBOARD PRINCIPAL ---
col1, col2, col3 = st.columns(3)

# Simulando dados (Substitua por requests.get(API_BASE_URL + "/status"))
try:
    # response = requests.get(f"{API_BASE_URL}/status").json()
    # stats = response['stats']
    stats = {"price": "64,230.50", "pnl": "+124.50", "activeGrids": 12, "decision": "Aumentando espaçamento da grade devido a volatilidade."}
    
    col1.metric("Preço Atual (BTC)", f"${stats['price']}")
    col2.metric("Lucro Total (PnL)", stats['pnl'], delta="2.15%")
    col3.metric("Grades Ativas", stats['activeGrids'])
except:
    st.warning("Aguardando conexão com o Backend...")

st.divider()

# Painel da IA Groq
st.markdown("### 🧠 Insight Groq AI")
st.info(f"**Decisão Atual:** {stats.get('decision', 'Analisando mercado...')}")

# Controle do Bot
col_btn1, col_btn2 = st.columns([1, 4])
with col_btn1:
    if st.button("🔄 Recarregar"):
        st.rerun()

# Tabela de Logs
st.markdown("### 📜 Logs de Execução Pionex")
log_data = [
    {"Tipo": "BUY", "Preço": "63,100", "Hora": "14:20", "Status": "Executado"},
    {"Tipo": "SELL", "Preço": "64,500", "Hora": "14:15", "Status": "Executado"},
    {"Tipo": "AI_ADJUST", "Preço": "---", "Hora": "12:00", "Status": "Recalibrando"},
]
st.table(pd.DataFrame(log_data))

# Auto-refresh (Opcional)
time.sleep(5)
st.rerun()
