from app.router.paths import dic_paths

import streamlit as st
import pandas as pd
from utils import *


st.set_page_config(layout="wide")


#-------------Importa todos os DFs necessários----------------
dic_paths = dic_paths()

st.session_state.df_vagas = import_df(dic_paths['csv_vagas_norm'])
st.session_state.df_requisitos = import_df(dic_paths['csv_requisitos'])


#-------------Cria as variáveis necessárias para os filtros----------------
lista_vagas_perfis = sorted(st.session_state.df_vagas['perfil_vaga'].unique().tolist())
lista_vagas_perfis.insert(0, 'Selecione')

lista_nivel = sorted(st.session_state.df_vagas['nivel_cargo'].unique().tolist())
lista_nivel.insert(0, 'Selecione')

lista_estado = sorted(st.session_state.df_vagas['estado'].unique().tolist())
lista_estado.insert(0, 'Selecione')

lista_empresa = sorted(st.session_state.df_vagas['empresa_contratante'].unique().tolist())
lista_empresa.insert(0, 'Selecione')


#-------------Cria a Barra de Filtros Lateral----------------
st.sidebar.header('Navegação')
page = st.sidebar.selectbox("",["Home", "Visualizar Vagas", "Análise Perfis Profissionais"])

st.sidebar.header('Filtros')
filtros_barra_lateral(lista_vagas_perfis, lista_nivel, lista_estado, lista_empresa)


#-------------Filtra os Dataframes----------------
st.session_state.df_vagas_filt = filtrar_df_vagas(st.session_state.df_vagas, st.session_state.filtro_perfil, st.session_state.filtro_nivel, st.session_state.filtro_uf, st.session_state.filtro_empresa)
st.session_state.df_ternario_filt = filtrar_df_vagas_ternario(st.session_state.df_vagas, st.session_state.filtro_nivel, st.session_state.filtro_uf, st.session_state.filtro_empresa)


#-------------Inicializa a página selecionada----------------
if page == "Home":
    import page_home as page_home
    page_home.exibir()
elif page == "Análise Perfis Profissionais":
    import page_perfis as page_perfis
    page_perfis.exibir()
elif page == "Visualizar Vagas":
    import page_vagas as page_vagas
    page_vagas.exibir()
