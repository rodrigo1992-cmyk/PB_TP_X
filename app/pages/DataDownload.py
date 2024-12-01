import streamlit as st
import pandas as pd
from utils import *
import csv

def control1():
    st.session_state.control = 1

def control0():
    if 'control' in st.session_state:
        del st.session_state.control
    if 'file_uploader' in st.session_state:
        del st.session_state['file_uploader']


def exibir():
    #Fazer upload de um arquivo CSV e apendar linhas ao dataframe

    #------------------------- CONTAINER DE DOWNLOAD DE BASES-----------------------------------
    df_vagas_filt = st.session_state.df_vagas_filt
    
    with st.expander(r"$\textsf{\LARGE \textbf{CONSULTAR E BAIXAR VAGAS}}$"):
        st.write("### Use o menu lateral para filtrar as vagas desejadas.")
        st.write(df_vagas_filt)

        #Converter o dataframe em csv
        csv = df_vagas_filt.to_csv(index=False, quotechar='"')
        st.download_button(label="Download CSV", data=csv, file_name='vagas_filtradas.csv', mime='text/csv')




    #------------------------- CONTAINER DE UPLOAD DE BASES-----------------------------------
    if 'control' not in st.session_state:
        st.session_state.control = 0
    
    with st.expander(r"$\textsf{\LARGE \textbf{CARREGAR NOVAS VAGAS}}$"):
        st.warning("🚨 ATENÇÃO Antes de carregar, confira se o arquivo possui as mesmas colunas da base atual. \nVocê pode baixar uma das vagas do Banco para confirmar o formato necessário para o arquivo. 🚨")

        if st.session_state.control == 0:
            st.button("Desejo Prosseguir",on_click=control1)

        if st.session_state.control == 1:
            uploaded_file = st.file_uploader(
                label = "Upload CSV", 
                key="file_uploader",
                type=['csv'], 
                label_visibility="hidden", 
                accept_multiple_files=False)

            api_post_new_vagas(uploaded_file)



    


