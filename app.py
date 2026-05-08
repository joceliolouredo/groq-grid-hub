import streamlit as st
import pandas as pd
import requests
import time

# ==============================================================================
# CONFIGURAÇÕES INICIAIS
# ==============================================================================
st.set_page_config(
    page_title="Groq Grid Hub", 
    page_icon="⚡", 
    layout="wide"
)

# SEU LINK OFICIAL DO RENDER (BACKEND)
API_BASE_URL = "https://groq-grid-hub.onrender.com" 

# CSS para Tema Dark Profissional
st.markdown("""
    <style>
    div[data-testid="stMetricValue"] {
        color: #818cf8 !important;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ GROQ GRID HUB")
st.subheader("AI-Driven Trading Control Panel")

# ==============================================================================
# 1. VERIFICAÇÃO DE CONEXÃO (HEALTH CHECK)
# ==============================================================================
try:
    health = requests.get(f"{API_BASE_URL}/health", timeout=10).json()
    st.markdown(f"""
        <div style="display: flex; gap: 20px; font-size: 14px; background: #1e293b; padding: 12px; border-radius: 15px; justify-content: center; color: white; border: 1px solid #334155;">
            <span style="color: #4ade80;">● Backend: Online</span> | 
            <span style="color: white;">Pionex: {health.get('pionex', 'Off')}</span> | 
            <span style="color: white;">Groq AI: {health.get('groq', 'Off')}</span>
        </div>
    """, unsafe_allow_html=True)
except Exception:
    st.error("🚨 Backend Offline - O servidor no Render pode estar despertando. Aguarde 30 segundos.")

# ==============================================================================
# 2. SIDEBAR (CONFIGURAÇÕES)
# ==============================================================================
st.sidebar.header("⚙️ Parâmetros da Grade")

# Busca de pares reais do Backend
try:
    pairs_response = requests.get(f"{API_BASE_URL}/pairs", timeout=5).json()
    available_pairs = pairs_response.get("pairs", ["BTC/USDT"])
except:
    available_pairs = ["BTC/USDT"]

pair = st.sidebar.selectbox("Par de Trading", available_pairs)
upper = st.sidebar.number_input("Limite Superior ($)", value=70000.0)
lower = st.sidebar.number_input("Limite Inferior ($)", value=60000.0)
count = st.sidebar.number_input("Quantidade de Grades", value=30)

if st.sidebar.button("💾 Salvar Configurações"):
    payload = {
        "symbol": pair,
        "upper_limit": upper,
        "lower_limit": lower,
        "grid_count": count
    }
    try:
        res = requests.post(f"{API_BASE_URL}/update-config", json=payload)
        if res.status_code == 200:
            st.sidebar.success(f"Configurado para {pair}!")
        else:
            st.sidebar.error("Erro na resposta do servidor")
    except:
        st.sidebar.error("Erro ao conectar na API")

# ==============================================================================
# 3. DASHBOARD PRINCIPAL
# ==============================================================================
try:
    # Busca dados reais do status do bot
    data = requests.get(f"{API_BASE_URL}/status", timeout=10).json()
    stats = data['stats']
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Preço Atual", f"${stats['price']}")
    col2.metric("Lucro Total (PnL)", stats['pnl'], delta="2.15%")
    col3.metric("Grades Ativas", stats['activeGrids'])

    st.divider()

    # Painel da IA Groq
    st.markdown("### 🧠 Insight Groq AI")
    st.info(f"**Decisão Atual:** {stats.get('decision', 'Analisando mercado...')}")

    # Controle do Bot
    btn_label = "⏹️ Parar Bot" if data.get('isRunning') else "▶️ Iniciar Bot"
    if st.button(btn_label):
        requests.post(f"{API_BASE_URL}/toggle-bot")
        st.rerun()

    # Tabela de Logs
    st.markdown("### 📜 Logs de Execução")
    if data.get('logs'):
        st.table(pd.DataFrame(data['logs']))
    else:
        st.write("Aguardando primeiras operações...")

except Exception as e:
    st.warning("Sincronizando dados com o servidor... Atualize em instantes.")

# Auto-refresh a cada 10 segundos
time.sleep(10)
st.rerun()
