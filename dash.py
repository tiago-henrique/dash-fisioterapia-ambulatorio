import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(layout='wide')

# -----------------------------
# CARREGAR DADOS
# -----------------------------
path = "https://imunogenetica.famerp.br/dash/ambulatorio_fisioterapia/indicadores.csv"
#path = "indicadores.csv"
df = pd.read_csv(path)

# -----------------------------
# MAPS
# -----------------------------
tipo_map = {
    'admisso': 'Admissão',
    'reavaliao': 'Reavaliação',
    'alta': 'Alta'
}

setor_map = {
    'urogenecologia': 'Urogenecologia',
    'musculoesqueletico': 'Muscoluesqueletico',
    'doencas_raras': 'Doenças raras',
    'neurologia_adulto': 'Neurologia adulto',
    'neuropediatria': 'Neuropediatria'
}

sexo_map = {1: 'Feminino', 2: 'Masculino'}
absorvido_map = {1: 'Sim', 0: 'Não'}
membro_map = {1: 'Membro superior', 2: 'Membro inferior'}

motivo_alta_map = {
    1: "Alta por término do programa de reabilitação",
    2: "Alta por abandono",
    3: "Alta por evasão",
    4: "Alta por intercorrência clínica ou social",
    5: "Alta a pedido",
    6: "Alta óbito",
    7: "Alta por falta",
}

# -----------------------------
# APLICAR MAPS
# -----------------------------
df['sexo'] = df['sexo'].map(sexo_map)
df['redcap_repeat_instrument'] = df['redcap_repeat_instrument'].map(tipo_map)
df['redcap_data_access_group'] = df['redcap_data_access_group'].map(setor_map)
df['paciente_absorvido'] = df['paciente_absorvido'].map(absorvido_map)
df['membro_avaliado'] = df['membro_avaliado'].map(membro_map)
df['motivo_alta'] = df['motivo_alta'].map(motivo_alta_map)

# -----------------------------
# DATAS
# -----------------------------
df['inicio_tratamento'] = pd.to_datetime(df['inicio_tratamento'], errors='coerce')

df['ano_inicio'] = df['inicio_tratamento'].dt.year
df['mes_inicio'] = df['inicio_tratamento'].dt.month

# -----------------------------
# MESES
# -----------------------------
meses_dict = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Filtros")

tipo = st.sidebar.selectbox(
    "Selecione o tipo",
    sorted(df['redcap_repeat_instrument'].dropna().unique())
)

setor = st.sidebar.selectbox(
    "Selecione o setor",
    sorted(df['redcap_data_access_group'].dropna().unique())
)

anos_inicio = sorted(df['ano_inicio'].dropna().unique())
ano_inicio_sel = st.sidebar.selectbox("Ano de início", anos_inicio)

meses_inicio_disponiveis = sorted(
    df[df['ano_inicio'] == ano_inicio_sel]['mes_inicio'].dropna().unique()
)

opcoes_meses = ['Todos'] + meses_inicio_disponiveis

mes_inicio_sel = st.sidebar.selectbox(
    "Mês de início",
    opcoes_meses,
    format_func=lambda x: "Todos os meses" if x == 'Todos' else meses_dict[x]
)

# -----------------------------
# FILTRAGEM
# -----------------------------
df_filtrado = df[
    (df['redcap_repeat_instrument'] == tipo) &
    (df['redcap_data_access_group'] == setor) &
    (df['ano_inicio'] == ano_inicio_sel)
]

if mes_inicio_sel != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['mes_inicio'] == mes_inicio_sel]

# -----------------------------
# TÍTULO
# -----------------------------
st.write(f"### {tipo} – {setor}")

if mes_inicio_sel == 'Todos':
    st.write(f"#### Ano completo de {ano_inicio_sel}")
else:
    st.write(f"#### {meses_dict[mes_inicio_sel]}/{ano_inicio_sel}")

# -----------------------------
# TABELA
# -----------------------------
df_exibicao = df_filtrado.drop(
    ['record_id', 'prontuario', 'nome_paciente'],
    axis=1,
    errors='ignore'
)

st.dataframe(df_exibicao)

# -----------------------------
# EVOLUÇÃO MENSAL
# -----------------------------
if mes_inicio_sel == 'Todos' and not df_filtrado.empty:
    st.write("#### Evolução mensal de registros")

    df_tempo = (
        df_filtrado
        .groupby('mes_inicio')
        .size()
        .reset_index(name='Quantidade')
    )

    df_tempo['Mês'] = df_tempo['mes_inicio'].map(meses_dict)

    st.plotly_chart(
        px.line(df_tempo, x='Mês', y='Quantidade', markers=True),
        use_container_width=True
    )

# -----------------------------
# GRÁFICOS POR TIPO
# -----------------------------
if not df_filtrado.empty:

    cols = st.columns(4)

    if tipo == 'Admissão':

        sexo = df_filtrado['sexo'].value_counts().reset_index()
        sexo.columns = ['Sexo', 'Quantidade']

        cid = df_filtrado['cid_principal'].value_counts().reset_index()
        cid.columns = ['CID', 'Quantidade']

        origem = df_filtrado['origem_encaminhamento'].value_counts().reset_index()
        origem.columns = ['Origem', 'Quantidade']

        absorvido = df_filtrado['paciente_absorvido'].value_counts().reset_index()
        absorvido.columns = ['Absorvido', 'Quantidade']

        with cols[0]:
            st.plotly_chart(px.pie(sexo, values='Quantidade', names='Sexo'), use_container_width=True)

        with cols[1]:
            st.plotly_chart(px.bar(cid, x='CID', y='Quantidade'), use_container_width=True)

        with cols[2]:
            st.plotly_chart(px.bar(origem, x='Origem', y='Quantidade'), use_container_width=True)

        with cols[3]:
            st.plotly_chart(px.bar(absorvido, x='Absorvido', y='Quantidade'), use_container_width=True)

    if tipo == 'Alta':

        motivo = df_filtrado['motivo_alta'].value_counts().reset_index()
        motivo.columns = ['Motivo da alta', 'Quantidade']

        st.plotly_chart(
            px.bar(motivo, x='Motivo da alta', y='Quantidade'),
            use_container_width=True
        )

else:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")

# -----------------------------
# DOWNLOAD
# -----------------------------
st.write("### Exportar dados")

excel_buffer = io.BytesIO()
df_filtrado.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)

st.download_button(
    label="Baixar Excel",
    data=excel_buffer,
    file_name="dados_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

