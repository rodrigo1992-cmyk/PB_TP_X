import sys
sys.path.append(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X')
from app.router.paths import *

import streamlit as st
import pandas as pd
from utils import *

dic_paths = dic_paths()


st.set_page_config(layout="wide")


#-------------Importa todos os DFs necessários----------------
df_vagas = import_df_vagas(dic_paths['csv_vagas_norm'])




#-------------Cria as variáveis necessárias para os filtros----------------
lista_vagas_perfis = sorted(df_vagas['perfil_vaga'].unique().tolist())
lista_vagas_perfis.insert(0, 'Selecione')

lista_nivel = sorted(df_vagas['nivel_cargo'].unique().tolist())
lista_nivel.insert(0, 'Selecione')

lista_estado = sorted(df_vagas['estado'].unique().tolist())
lista_estado.insert(0, 'Selecione')

lista_empresa = sorted(df_vagas['empresa_contratante'].unique().tolist())
lista_empresa.insert(0, 'Selecione')



#-------------Cria a Barra de Filtros Lateral----------------
st.sidebar.header('Navegação')
page = st.sidebar.selectbox("",["page_a", "page_b"])

st.sidebar.header('Filtros')
filtros_barra_lateral(lista_vagas_perfis, lista_nivel, lista_estado, lista_empresa)


#-------------Inicializa a página selecionada----------------
if page == "page_a":
    import page_a
    page_a.exibir()
elif page == "Análise de Jogadores":
    import page_b
    page_b.exibir()
