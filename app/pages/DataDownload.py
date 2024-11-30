import streamlit as st
import pandas as pd
from utils import *

def exibir():
    #Fazer upload de um arquivo CSV e apendar linhas ao dataframe
    st.write("#### Se desejar, você pode fazer upload de um arquivo CSV com novas vagas e adicionar ao dataframe.")
    st.write("ATENÇÃO: Antes de carregar, confira se o arquivo possui as mesmas colunas do dataframe atual.")
    new_rows = st.file_uploader("Upload CSV", type=['csv'])
    new_df = None
    
    if new_rows is not None:
        new_df = pd.read_csv(new_rows) 
    
    api_post_new_vagas(new_df)
    #Converter o dataframe em csv
    csv = st.session_state.df_vagas_filt.to_csv(index=False, quotechar='"')
    st.download_button(label="Download CSV", data=csv, file_name='vagas_filtradas.csv', mime='text/csv')
    


