from app.router.paths import *

import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from utils import *

st.set_page_config(layout="wide", page_title="DataJob Finder", page_icon="🔎")

if 'load_app' not in st.session_state:
    st.session_state.load_app = 1
    progress_bar(5,"Inicializando o Aplicativo")

#-------------Importa todos os DFs necessários----------------
try: 
    st.session_state.df_vagas = api_get_file_vagas_norm()

except Exception as e:
    st.error(f"Falha na requisição à API para obtenção da base de vagas. {e}", icon="🚨", )
    st.stop()

try: st.session_state.df_requisitos = api_get_file_requisitos()
except Exception as e:
    st.error(f"Falha na requisição à API para obtenção da base de requisitos. {e}", icon="🚨", )
    st.stop()


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
page = st.sidebar.selectbox("nav",["About", "Job Finder", "Profile Analysis", "Data Download"],label_visibility="hidden")

if page == "Profile Analysis" or page == "Data Download":
    st.sidebar.header('Filtros')
    filtros_barra_lateral(lista_vagas_perfis, lista_nivel, lista_estado, lista_empresa)


    #-------------Filtra os Dataframes----------------
    st.session_state.df_vagas_filt = filtrar_df_vagas(st.session_state.df_vagas, st.session_state.filtro_perfil, st.session_state.filtro_nivel, st.session_state.filtro_uf, st.session_state.filtro_empresa)
    st.session_state.df_ternario_filt = filtrar_df_vagas_ternario(st.session_state.df_vagas, st.session_state.filtro_nivel, st.session_state.filtro_uf, st.session_state.filtro_empresa)



#-------------Inicializa a página selecionada----------------
if page == "About":
    import About as About
    About.exibir()
elif page == "Job Finder":
    import JobFinder as JobFinder
    JobFinder.exibir()
elif page == "Profile Analysis":
    import ProfileAnalysis as ProfileAnalysis
    ProfileAnalysis.exibir()
elif page == "Data Download":
    import app.pages.DataDownload as DataDownload
    DataDownload.exibir()