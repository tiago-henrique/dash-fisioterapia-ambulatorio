import streamlit as st
import pandas as pd
import plotly.express as px
import io

st.set_page_config(layout='wide')

path = ("https://imunogenetica.famerp.br/dash/ambulatorio_fisioterapia/indicadores.csv")
df = pd.read_csv(path)
 
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
sexo_map = {
    1: 'Feminino',
    2: 'Masculino'
}
absorvido_map = {
    1: 'Sim',
    0: 'Não'
}
membro_map = {
    1: 'Membro superior',
    2: 'Membro inferior'
}

df['sexo'] = df['sexo'].map(sexo_map)
df['redcap_repeat_instrument'] = df['redcap_repeat_instrument'].map(tipo_map)
df['redcap_data_access_group'] = df['redcap_data_access_group'].map(setor_map)
df['paciente_absorvido'] = df['paciente_absorvido'].map(absorvido_map)
df['membro_avaliado'] = df['membro_avaliado'].map(membro_map)

tipo = st.sidebar.selectbox('Selecione o tipo', ('Admissão', 'Reavaliação', 'Alta'))
setores = df['redcap_data_access_group'].dropna().unique()
setor = st.sidebar.selectbox('Selecione o setor', setores)

df_filtrado = df[
    (df['redcap_repeat_instrument'] == tipo) &
    (df['redcap_data_access_group'] == setor)
]

st.write(f"### Registros de {tipo} - Setor: {setor}")
df_filtrado.drop(['record_id', 'prontuario', 'nome_paciente'], axis=1, inplace=True)

st.write("#### Dados filtrados")
st.dataframe(df_filtrado)

st.write("#### Distribuição de registros por setor")
df_setor_count = df['redcap_data_access_group'].value_counts().reset_index()
df_setor_count.columns = ['Setor', 'Quantidade']
st.bar_chart(df_setor_count.set_index('Setor'))


col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)
col7, col8 = st.columns(2)
col9, col10 = st.columns(2)
col11, col12 = st.columns(2)
col13, col14 = st.columns(2)
col15, col16 = st.columns(2)


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

        forca_muscular_final = df_filtrado['forca_muscular_final'].value_counts().reset_index()
        forca_muscular_final.columns = ['Força muscular final', 'Quantidade']

        dash_inicial = df_filtrado['dash_inicial'].value_counts().reset_index()
        dash_inicial.columns = ['Dash inicial', 'Quantidade']

        dash_final = df_filtrado['dash_final'].value_counts().reset_index()
        dash_final.columns = ['Dash final', 'Quantidade']
        
        tinetti_inicial = df_filtrado['tinetti_inicial'].value_counts().reset_index()
        tinetti_inicial.columns = ['Tinetti inicial', 'Quantidade']

        tinetti_final = df_filtrado['tinetti_final'].value_counts().reset_index()
        tinetti_final.columns = ['Tinetti final', 'Quantidade']

        tug_inicial = df_filtrado['tug_teste_inicial'].value_counts().reset_index()
        tug_inicial.columns = ['Tug inicial', 'Quantidade']

        tug_final = df_filtrado['teste_tug_final'].value_counts().reset_index()
        tug_final.columns = ['Tug final', 'Quantidade']

        forca_mi = df_filtrado['forca_mi'].value_counts().reset_index()
        forca_mi.columns = ['Força', 'Quantidade']

        forca_mi_final = df_filtrado['forca_mi_final'].value_counts().reset_index()
        forca_mi_final.columns = ['Força membro inferior final', 'Quantidade']

        with col1:
            st.write("#### Distribuição por sexo")
            fig_sexo = px.pie(sexo, values='Quantidade', names='Sexo', color="Sexo")
            st.plotly_chart(fig_sexo, use_container_width=True)

        with col2:
            st.write("#### CID Principal")
            fig_cid = px.bar(cid, x='CID Principal', y='Quantidade', color='CID Principal')
            st.plotly_chart(fig_cid, use_container_width=True)

        if not origem.empty:
            with col3:
                st.write("#### Distribuição por origem / encaminhamento")
                fig_origem = px.bar(origem, x='Origem', y='Quantidade', color="Origem")
                st.plotly_chart(fig_origem, use_container_width=True)
        
        if not absorvido.empty:
            with col4:
                st.write("#### Pacientes absorvidos")
                fig_absorvido = px.bar(absorvido, x='Absorvido', y='Quantidade')
                st.plotly_chart(fig_absorvido, use_container_width=True)
        
        if not membro.empty:
            with col5:
                st.write("#### Membro avaliado")
                fig_membro = px.bar(membro, x='Membro avaliado', y='Quantidade')
                st.plotly_chart(fig_membro, use_container_width=True)
        
        if not tempo_tratamento.empty:
            with col6:
                st.write("#### Tempo de tratamento")
                fig_tempo_tratamento = px.bar(tempo_tratamento, x='Tempo tratamento', y='Quantidade')
                st.plotly_chart(fig_tempo_tratamento, use_container_width=True)

        if not forca_muscular_inicial.empty:
            with col7:
                st.write('#### Força muscular inicial')
                fig_forca_muscular_inicial = px.bar(forca_muscular_inicial, x='Força muscular inicial', y='Quantidade')
                st.plotly_chart(fig_forca_muscular_inicial, use_container_width=True)

        if not forca_muscular_final.empty:
            with col8:
                st.write('#### Força muscular final')
                fig_forca_muscular_final = px.bar(forca_muscular_final, x='Força muscular final', y='Quantidade')
                st.plotly_chart(fig_forca_muscular_final, use_container_width=True)

        if not dash_inicial.empty:
            with col9:
                st.write('#### Dash inicial')
                fig_dash_inicial = px.bar(dash_inicial, x='Dash inicial', y='Quantidade')
                st.plotly_chart(fig_dash_inicial, use_container_width=True)

        if not dash_final.empty:
            with col10:
                st.write('#### Dash final')
                fig_dash_final = px.bar(dash_final, x='Dash final', y='Quantidade')
                st.plotly_chart(fig_dash_final, use_container_width=True)

        if not tinetti_inicial.empty:
            with col11:
                st.write("#### Tinetti inicial")
                fig_tinetti_inicial = px.bar(tinetti_inicial, x='Tinetti inicial', y='Quantidade')
                st.plotly_chart(fig_tinetti_inicial, use_container_width=True)

        if not tinetti_final.empty:
            with col12:
                st.write("#### Tinetti final")
                fig_tinetti_final = px.bar(tinetti_final, x='Tinetti final', y='Quantidade')
                st.plotly_chart(fig_tinetti_final, use_container_width=True)

        if not tug_inicial.empty:
            with col13:
                st.write("#### Tug teste inicial")
                fig_tug_inicial = px.bar(tug_inicial, x='Tug inicial', y='Quantidade')
                st.plotly_chart(fig_tug_inicial, use_container_width=True)

        if not tug_final.empty:
            with col14:
                st.write("#### Tug teste final")
                fig_tug_final = px.bar(tug_final, x='Tug final', y='Quantidade')
                st.plotly_chart(fig_tug_final, use_container_width=True)

        if not forca_mi.empty:
            with col15:
                st.write("#### Força membro inferior inicial")
                fig_forca_mi = px.bar(forca_mi, x='Força', y='Quantidade', color='Força')
                st.plotly_chart(fig_forca_mi, use_container_width=True)
        
        if not forca_mi_final.empty:
            with col16:
                st.write("#### Força membro inferior final ")
                fig_forca_mi_final = px.bar(forca_mi_final, x='Força membro inferior final', y='Quantidade', color='Força')
                st.plotly_chart(fig_forca_mi_final, use_container_width=True)
        
else:
    st.warning("Nenhum registro encontrado para os filtros selecionados.")

st.write("Gerar arquivo excel com os dados analisados:")
#st.dataframe(df_filtrado)

excel_buffer = io.BytesIO()
df_filtrado.to_excel(excel_buffer, index=False)
excel_buffer.seek(0)

st.download_button(
    label="Baixar como .xlsx",
    data=excel_buffer,
    file_name="meus_dados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
