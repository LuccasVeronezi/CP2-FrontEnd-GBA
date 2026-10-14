# Arquivo: app.py
import streamlit as st
import requests
import pandas as pd
import uuid

# Configuração da página
st.set_page_config(page_title="Forzy Digital Twin - Sensores", layout="wide")

# Gerar um Session ID único para o usuário atual (se não existir na sessão do Streamlit)
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

API_BASE_URL = "http://localhost:8000/v1"

# Função auxiliar para fazer o request passando os headers de observabilidade
def fazer_requisicao(endpoint, feature_name):
    headers = {
        "X-Session-Id": st.session_state["session_id"],
        "X-Feature": feature_name
    }
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
        return None

# Interface
st.title("🏭 Forzy · Digital Twin - Monitoramento de Sensores")
st.write(f"**Sessão atual:** `{st.session_state['session_id']}`")

tag_sensor = st.text_input("Tag do Sensor", value="SENSOR-XYZ-01")

# Criação das abas da interface
aba1, aba2, aba3 = st.tabs(["📡 Leitura Atual", "📊 Histórico", "🔍 Observabilidade (Governança)"])

with aba1:
    st.header("Leitura Atual do Sensor")
    if st.button("Buscar Leitura"):
        dados = fazer_requisicao(f"/sensores/{tag_sensor}/leitura-atual", "Tela_Leitura_Atual")
        if dados:
            col1, col2 = st.columns(2)
            col1.metric("Valor Registrado", f"{dados['leitura']} °C")
            
            cor = "green" if dados['severidade'] == "Normal" else "red"
            col2.markdown(f"### Severidade: :{cor}[{dados['severidade']}]")

with aba2:
    st.header("Histórico de Leituras")
    if st.button("Carregar Histórico"):
        dados = fazer_requisicao(f"/sensores/{tag_sensor}/historico", "Tela_Historico")
        if dados and dados.get("historico"):
            df = pd.DataFrame(dados["historico"])
            st.dataframe(df, use_container_width=True)
            st.line_chart(df.set_index("timestamp")["valor"])

with aba3:
    st.header("Relatório de Observabilidade")
    st.info("Estes dados são consumidos pela disciplina de Governança em IA para auditar o contrato de métricas.")
    if st.button("Carregar Logs de Auditoria"):
        dados = fazer_requisicao("/observabilidade", "Tela_Observabilidade")
        if dados and dados.get("logs"):
            st.metric("Total de Requisições Capturadas", dados["total_registros"])
            df_logs = pd.DataFrame(dados["logs"])
            st.dataframe(df_logs, use_container_width=True)