import streamlit as st
import pandas as pd

def exibir():
    st.title("Visualização das Vagas Anunciadas")

    #Fazer upload de um arquivo CSV e apendar linhas ao dataframe
    st.write("#### Se desejar, você pode fazer upload de um arquivo CSV com novas vagas e adicionar ao dataframe.")
    st.write("ATENÇÃO: Antes de carregar, confira se o arquivo possui as mesmas colunas do dataframe atual.")
    new_file = st.file_uploader("Upload CSV", type=['csv'])

    if new_file is not None:
        new_df = pd.read_csv(new_file)
        
        #Conferir se as colunas são iguais
        colunas_df_old = new_df.columns.tolist()
        colunas_df_new =  st.session_state.df_vagas_filt.columns.tolist()
        if colunas_df_new != colunas_df_old:
            st.error("As colunas do arquivo não são iguais às do dataframe atual.",icon="🚨")
            st.stop()
        
        #Conferir se o id_vaga já existe
        elif new_df['id_vaga'].isin(st.session_state.df_vagas_filt['id_vaga']).any():
            st.error("Uma ou mais das vagas carregadas já estão contida no dataframe atual.",icon="🚨")
            st.stop()
        
        #Se passar nas validações, concatenar ao dataframe atual
        else:
            st.session_state.df_vagas_filt = pd.concat([st.session_state.df_vagas_filt, new_df], ignore_index=True)
            st.success("Vagas adicionadas com sucesso!")
    
    st.dataframe(st.session_state.df_vagas_filt, height = 500)

    #Converter o dataframe em csv
    csv = st.session_state.df_vagas_filt.to_csv(index=False, quotechar='"')
    st.download_button(label="Download CSV", data=csv, file_name='vagas_filtradas.csv', mime='text/csv')
    
