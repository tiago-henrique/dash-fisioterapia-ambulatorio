import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(layout='wide')

# -----------------------------
# CARREGAR DADOS
# -----------------------------
path = ("https://imunogenetica.famerp.br/dash/ambulatorio_fisioterapia/indicadores.csv")
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
# FILTROS DE DATA
# -----------------------------
df['inicio_tratamento'] = pd.to_datetime(df['inicio_tratamento'], errors='coerce')
df['termino_tratamento'] = pd.to_datetime(df['termino_tratamento'], errors='coerce')

df['ano_inicio'] = df['inicio_tratamento'].dt.year
df['mes_inicio'] = df['inicio_tratamento'].dt.month

#df['ano_fim'] = df['termino_tratamento'].dt.year
#df['mes_fim'] = df['termino_tratamento'].dt.month

# Meses por extenso
meses_dict = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

# -----------------------------
# SIDEBAR — FILTROS
# -----------------------------
tipo = st.sidebar.selectbox('Selecione o tipo', ('Admissão', 'Reavaliação', 'Alta'))

setores = df['redcap_data_access_group'].dropna().unique()
setor = st.sidebar.selectbox('Selecione o setor', setores)

# Filtros de início do tratamento
anos_inicio = sorted(df['ano_inicio'].dropna().unique())
ano_inicio_sel = st.sidebar.selectbox("Ano de início", anos_inicio)

meses_inicio_disponiveis = sorted(df[df['ano_inicio'] == ano_inicio_sel]['mes_inicio'].dropna().unique())
mes_inicio_sel = st.sidebar.selectbox("Mês de início", meses_inicio_disponiveis, format_func=lambda x: meses_dict[x])

# Filtros de término do tratamento
#st.sidebar.markdown("---")
#st.sidebar.markdown("### Término do tratamento")

#anos_fim = sorted(df['ano_fim'].dropna().unique())
#ano_fim_sel = st.sidebar.selectbox("Ano de término", anos_fim)

#meses_fim_disponiveis = sorted(df[df['ano_fim'] == ano_fim_sel]['mes_fim'].dropna().unique())
#mes_fim_sel = st.sidebar.selectbox("Mês de término", meses_fim_disponiveis, format_func=lambda x: meses_dict[x])

# -----------------------------
# APLICAR FILTROS
# -----------------------------
#df_filtrado = df[
#    (df['redcap_repeat_instrument'] == tipo) &
#    (df['redcap_data_access_group'] == setor) &
#    (df['ano_inicio'] == ano_inicio_sel) &
#    (df['mes_inicio'] == mes_inicio_sel) &
#    (df['ano_fim'] == ano_fim_sel) &
#    (df['mes_fim'] == mes_fim_sel)
#]

df_filtrado = df[
    (df['redcap_repeat_instrument'] == tipo) &
    (df['redcap_data_access_group'] == setor) &
    (df['ano_inicio'] == ano_inicio_sel) &
    (df['mes_inicio'] == mes_inicio_sel) 
]

# -----------------------------
# EXIBIÇÃO
# -----------------------------
st.write(f"### {tipo} – {setor}")
st.write(f"#### Início: {meses_dict[mes_inicio_sel]}/{ano_inicio_sel}")

df_filtrado = df_filtrado.drop(['record_id', 'prontuario', 'nome_paciente'], axis=1, errors='ignore')

st.write("#### Dados filtrados")
st.dataframe(df_filtrado)

# -----------------------------
# GRÁFICO DE SETORES
# -----------------------------
st.write("#### Distribuição de registros por setor")
df_setor_count = df['redcap_data_access_group'].value_counts().reset_index()
df_setor_count.columns = ['Setor', 'Quantidade']
st.bar_chart(df_setor_count.set_index('Setor'))

# -----------------------------
# LAYOUT DE GRÁFICOS
# -----------------------------
cols = [st.columns(2) for _ in range(10)]
cols = sum(cols, [])

# -----------------------------
# GRÁFICOS — ADMISSÃO
# -----------------------------
if not df_filtrado.empty:
    if tipo == 'Admissão':

        sexo = df_filtrado['sexo'].value_counts().reset_index()
        sexo.columns = ['Sexo', 'Quantidade']

        cid = df_filtrado['cid_principal'].value_counts().reset_index()
        cid.columns = ['CID Principal', 'Quantidade']

        origem = df_filtrado['origem_encaminhamento'].value_counts().reset_index()
        origem.columns = ['Origem', 'Quantidade']

        absorvido = df_filtrado['paciente_absorvido'].value_counts().reset_index()
        absorvido.columns = ['Absorvido', 'Quantidade']

        membro = df_filtrado['membro_avaliado'].value_counts().reset_index()
        membro.columns = ['Membro avaliado', 'Quantidade']

        tempo_tratamento = df_filtrado['tempo_tratamento'].value_counts().reset_index()
        tempo_tratamento.columns = ['Tempo tratamento', 'Quantidade']

        forca_muscular_inicial = df_filtrado['forca_muscular_inicial'].value_counts().reset_index()
        forca_muscular_inicial.columns = ['Força muscular inicial', 'Quantidade']

        with cols[0]:
            st.write("#### Distribuição por sexo")
            st.plotly_chart(px.pie(sexo, values='Quantidade', names='Sexo'), use_container_width=True)

        with cols[1]:
            st.write("#### CID Principal")
            st.plotly_chart(px.bar(cid, x='CID Principal', y='Quantidade'), use_container_width=True)

        with cols[2]:
            st.write("#### Origem do encaminhamento")
            st.plotly_chart(px.bar(origem, x='Origem', y='Quantidade'), use_container_width=True)

        with cols[3]:
            st.write("#### Pacientes absorvidos")
            st.plotly_chart(px.bar(absorvido, x='Absorvido', y='Quantidade'), use_container_width=True)

    if tipo == 'Alta':
        motivo_alta = df_filtrado['motivo_alta'].value_counts().reset_index()
        motivo_alta.columns = ['Motivo alta', 'Quantidade']

        with cols[5]:
            st.write("#### Motivo da alta")
            st.plotly_chart(px.bar(motivo_alta, x='Motivo alta', y='Quantidade'), use_container_width=True)

else:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")

# -----------------------------
# DOWNLOAD DO EXCEL
# -----------------------------
st.write("Gerar arquivo excel com os dados analisados:")

excel_buffer = io.BytesIO()
df_filtrado.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)

st.download_button(
    label="Baixar como .xlsx",
    data=excel_buffer,
    file_name="dados_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

