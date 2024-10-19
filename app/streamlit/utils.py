
import streamlit as st
import pandas as pd

def import_df_vagas(path_vagas):
    df_vagas = pd.read_csv(path_vagas)
    return df_vagas

def filtros_barra_lateral(lista_vagas: list, lista_nivel: list, lista_uf: list, lista_empresa: list):

    '''Função que cria os filtros na barra lateral da aplicação
        Args:
            lista_vagas (list): Lista os perfis distintos das vagas
    '''
    #Inicializo as variáveis de sessão
    if 'filtro_perfil' not in st.session_state:
        st.session_state.filtro_perfil = 'Selecione'
    
    if 'filtro_nivel' not in st.session_state:
        st.session_state.filtro_nivel = 'Selecione'
    
    if 'filtro_uf' not in st.session_state:
        st.session_state.filtro_uf = 'Selecione'
    
    if 'filtro_empresa' not in st.session_state:
        st.session_state.filtro_empresa = 'Selecione'

    #Crio o Seletor
    st.session_state.filtro_perfil = st.sidebar.selectbox('Filtrar Perfil da Vaga', lista_vagas, key='1')
    st.session_state.filtro_nivel = st.sidebar.selectbox('Filtrar Nível da Vaga', lista_nivel, key='2')
    st.session_state.filtro_uf = st.sidebar.selectbox('Filtrar Estado', lista_uf, key='3')
    st.session_state.filtro_empresa = st.sidebar.selectbox('Filtrar Empresa', lista_empresa, key='4')
