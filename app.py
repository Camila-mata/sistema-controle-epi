import streamlit as st
from streamlit_drawable_canvas import st_canvas
from ficha_epi import gerar_ficha
from database import criar_tabela, conectar
from PIL import Image
import pandas as pd
from datetime import datetime, timedelta
import os
import sqlite3


# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================
st.set_page_config(
    page_title="Sistema de Controle de EPI",
    page_icon="🦺",
    layout="wide"
)
# ======================
# ESTILO
# ======================
st.markdown("""
<style>
.stApp { background-color: #0B0F19; color: white; }
header { background-color: #0B0F19 !important; }
[data-testid="stHeader"] { background-color: #0B0F19; }
section[data-testid="stSidebar"] { background-color: #111827; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p { color: #E5E7EB !important; }
input, textarea { color: white !important; }
div[data-baseweb="input"] > div { background-color: #1F2937 !important; color: white !important; }
div[data-baseweb="select"] div { color: white !important; background-color: #1F2937 !important; }
.stButton>button { background-color: #2563EB; color: white; border-radius: 8px; }
[data-testid="stDataFrame"] { background-color: #1F2937; color: white; }
input[type="date"] { color: white !important; }
label { color: #E5E7EB !important; font-weight: 500; }
::placeholder { color: #9CA3AF !important; }
</style>
""", unsafe_allow_html=True)
# ======================
# BANCO DE DADOS
# ======================
criar_tabela()  # garante que todas as tabelas existem
conn = conectar()
cursor = conn.cursor()
# verifica se a coluna status existe na tabela funcionarios
try:
    cursor.execute("SELECT status FROM funcionarios LIMIT 1")
except sqlite3.OperationalError:
    cursor.execute("ALTER TABLE funcionarios ADD COLUMN status TEXT DEFAULT 'Ativo'")
    conn.commit()
# ======================
# SIDEBAR
# ======================
st.sidebar.title("🦺 Controle de EPI")
menu = st.sidebar.selectbox(
    "Navegação",
    ["Dashboard", "Funcionários", "EPIs", "Entrega de EPI"]
)
st.sidebar.markdown("---")
st.sidebar.info("Sistema de gestão de EPIs conforme NR-06")
# ======================
# DASHBOARD
# ======================
if menu == "Dashboard":
    st.header("📊 Dashboard de Segurança")
    cursor.execute("SELECT funcionario, epi, data FROM entregas")
    dados = cursor.fetchall()
    df = pd.DataFrame(dados, columns=["Funcionário", "EPI", "Data"])
    if df.empty:
        st.info("Nenhuma entrega registrada ainda.")
    else:
        # filtro por funcionário com "Todos"
        funcionarios = ["Todos"] + list(df["Funcionário"].unique())
        filtro_func = st.multiselect("Filtrar por funcionário", funcionarios, default=["Todos"])
        if "Todos" in filtro_func:
            df_filtrado = df.copy()
        else:
            df_filtrado = df[df["Funcionário"].isin(filtro_func)]
        # filtro por data
        data_min = pd.to_datetime(df_filtrado["Data"]).min()
        data_max = pd.to_datetime(df_filtrado["Data"]).max()
        filtro_datas = st.date_input("Filtrar por data", [data_min, data_max])
        if len(filtro_datas) == 2:
            df_filtrado = df_filtrado[
                (pd.to_datetime(df_filtrado["Data"]) >= pd.to_datetime(filtro_datas[0])) &
                (pd.to_datetime(df_filtrado["Data"]) <= pd.to_datetime(filtro_datas[1]))
            ]
        # métricas
        total_entregas = len(df_filtrado)
        total_funcionarios = df_filtrado["Funcionário"].nunique()
        total_epis = df_filtrado["EPI"].nunique()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de entregas", total_entregas)
        col2.metric("Funcionários atendidos", total_funcionarios)
        col3.metric("Tipos de EPI", total_epis)
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("EPIs mais entregues")
            grafico_epi = df_filtrado["EPI"].value_counts()
            st.bar_chart(grafico_epi)
        with col2:
            st.subheader("Entregas por funcionário")
            grafico_func = df_filtrado["Funcionário"].value_counts()
            st.bar_chart(grafico_func)
        st.divider()
        st.subheader("Histórico completo")
        st.dataframe(df_filtrado)
        csv = df_filtrado.to_csv(index=False).encode("utf-8")
        st.download_button("Exportar histórico (CSV)", data=csv, file_name="historico_entregas.csv", mime="text/csv")
# ======================
# FUNCIONÁRIOS
# ======================
elif menu == "Funcionários":
    st.header("Cadastro de Funcionário")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        nome = st.text_input("Nome")
    with col2:
        cargo = st.text_input("Cargo")
    with col3:
        setor = st.text_input("Setor")
    with col4:
        status = st.selectbox("Status", ["Ativo", "Desligado"])
    if st.button("Cadastrar Funcionário"):
        cursor.execute("""
        INSERT INTO funcionarios (nome, cargo, setor, status)
        VALUES (?, ?, ?, ?)
        """, (nome, cargo, setor, status))
        conn.commit()
        st.success(f"Funcionário {nome} cadastrado com status {status}!")
    st.subheader("Funcionários cadastrados")
    cursor.execute("SELECT id, nome, cargo, setor, status FROM funcionarios")
    funcionarios = cursor.fetchall()
    df_func = pd.DataFrame(funcionarios, columns=["ID", "Nome", "Cargo", "Setor", "Status"])
    st.dataframe(df_func)
    csv = df_func.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar Funcionários (CSV)", data=csv, file_name="funcionarios.csv", mime="text/csv")
# ======================
# EPIs
# ======================
elif menu == "EPIs":
    st.header("Cadastro de EPI")
    col1, col2 = st.columns(2)
    with col1:
        nome_epi = st.text_input("Nome do EPI")
        ca = st.text_input("CA")
    with col2:
        validade_dias = st.number_input("Validade do EPI (dias)", min_value=1)
        fabricante = st.text_input("Fabricante")
    if st.button("Cadastrar EPI"):
        cursor.execute("""
        INSERT INTO epis (nome, ca, validade_dias, fabricante)
        VALUES (?, ?, ?, ?)
        """, (nome_epi, ca, validade_dias, fabricante))
        conn.commit()
        st.success("EPI cadastrado!")
    st.subheader("EPIs cadastrados")
    cursor.execute("SELECT id, nome, ca, validade_dias, fabricante FROM epis")
    epis = cursor.fetchall()
    df_epi = pd.DataFrame(epis, columns=["ID", "EPI", "CA", "Validade (dias)", "Fabricante"])
    st.dataframe(df_epi)
    csv = df_epi.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar EPIs (CSV)", data=csv, file_name="epis.csv", mime="text/csv")
# ======================
# ENTREGA DE EPI
# ======================
elif menu == "Entrega de EPI":
    st.header("Entrega de EPI")

    cursor.execute("SELECT nome FROM funcionarios WHERE status='Ativo'")
    funcionarios = [f[0] for f in cursor.fetchall()]
    cursor.execute("SELECT nome FROM epis")
    epis = [e[0] for e in cursor.fetchall()]
    col1, col2, col3 = st.columns(3)
    with col1:
        funcionario = st.selectbox("Funcionário", funcionarios)
    with col2:
        epi = st.selectbox("EPI", epis)
    with col3:
        data = st.date_input("Data da entrega")
    st.subheader("Assinatura do Funcionário")
    canvas_result = st_canvas(
        stroke_width=2,
        stroke_color="black",
        background_color="white",
        height=150,
        width=400,
        drawing_mode="freedraw",
        key="assinatura",
    )
    if st.button("Registrar Entrega"):
        cursor.execute("SELECT validade_dias FROM epis WHERE nome = ?", (epi,))
        validade_dias = cursor.fetchone()[0]
        vencimento = data + timedelta(days=validade_dias)
        cursor.execute("""
        INSERT INTO entregas (funcionario, epi, data, vencimento)
        VALUES (?, ?, ?, ?)
        """, (funcionario, epi, str(data), str(vencimento)))
        conn.commit()
        assinatura_path = None
        if canvas_result.image_data is not None:
            assinatura = Image.fromarray(canvas_result.image_data.astype("uint8"))
            os.makedirs("assinaturas", exist_ok=True)
            assinatura_path = f"assinaturas/assinatura_{funcionario}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            assinatura.save(assinatura_path)
        arquivo = gerar_ficha(funcionario, epi, data, assinatura_path)
        st.success("Entrega registrada!")
        with open(arquivo, "rb") as file:
            st.download_button(
                label="Baixar Ficha de EPI",
                data=file,
                file_name=arquivo,
                mime="application/pdf"
            )
# ======================
# HISTÓRICO E ALERTAS
# ======================
st.subheader("Histórico de entregas")
cursor.execute("SELECT funcionario, epi, data, vencimento FROM entregas")
entregas = cursor.fetchall()
df_entregas = pd.DataFrame(entregas, columns=["Funcionário", "EPI", "Data", "Vencimento"])
st.dataframe(df_entregas)
csv = df_entregas.to_csv(index=False).encode("utf-8")
st.download_button("Exportar Histórico de Entregas (CSV)", data=csv, file_name="historico_entregas.csv", mime="text/csv")
st.subheader("Alertas de vencimento")
hoje = datetime.today()
for e in entregas:
    funcionario, epi, data_entrega, vencimento_str = e
    vencimento = datetime.strptime(vencimento_str, "%Y-%m-%d")
    dias = (vencimento - hoje).days
    if dias < 0:
        st.error(f"{epi} de {funcionario} está VENCIDO")
    elif dias <= 5:
        st.warning(f"{epi} de {funcionario} vence em {dias} dias")