import streamlit as st
import pandas as pd
import requests
import time
import random

#-----------------------------------------------CHAMADAS A APIS----------------------------------------------------
@st.cache_data
def api_get_file_vagas_norm():
    '''
    Função que acessa a API para pegar o arquivo vagas_norm.csv
    '''

    response = requests.get("http://localhost:8000/csv_vagas_norm")
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df['id_vaga'] = pd.to_numeric(df['id_vaga'], errors='coerce')
        df['salario'] = pd.to_numeric(df['salario'], errors='coerce')

        return df
    else:
        st.error("Erro ao acessar a API: {}".format(response.status_code))







@st.cache_data
def api_get_file_requisitos():
    '''
    Função que acessa a API para pegar o arquivo requisitos.csv
    '''

    response = requests.get("http://localhost:8000/csv_requisitos")
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df['id_vaga'] = pd.to_numeric(df['id_vaga'], errors='coerce')

        return df
    else:
        st.error("Erro ao acessar a API: {}".format(response.status_code))








def api_post_new_vagas(new_df):
    df_vagas_filt = st.session_state.df_vagas

    if new_df is not None:
    
        st.title('Pré-Visualização das linhas a serem carregadas')

        #converter o dataframe em dicionário
        new_rows = new_df.to_dict(orient='records')
        
        # No Json os valores NaN devem ser convertidos para None (Em campos de String) e para Zero (em campos numéricos)
        processed_rows = []
        for row in new_rows:
            processed_row = {}
            for key, value in row.items():
                if pd.notna(value):
                    processed_row[key] = value
                else:
                    # Devo adicionar aqui a identificação de todos os campos numéricos que devem ser convertidos para 0
                    if key == 'salario':
                        processed_row[key] = 0
                    else:
                        processed_row[key] = None
            
            processed_rows.append(processed_row)

        try:
            response = requests.post("http://localhost:8000/api_post_new_vagas", json=processed_rows)
            response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx

            st.success("Vagas adicionadas com sucesso!")
            st.session_state.df_vagas = api_get_file_vagas_norm()
            df_vagas_filt = st.session_state.df_vagas

        except requests.exceptions.HTTPError as http_err:
            # Captura o erro e exibe a mensagem de detalhe
            error_detail = http_err.response.json().get("detail", "Erro desconhecido.")
            st.error(f"Erro: {error_detail}", icon="🚨")


    st.dataframe(df_vagas_filt, height = 500)



def api_post_llm_search(search_sentence):

    dict = {'text': search_sentence}
    print("Input convertido em dict, será realizado o request")

    response = requests.post("http://localhost:8000/api_llm_search", json=dict)
    
    if response.status_code == 200:
        print("Resposta recebida com sucesso")

        response = response.json()

        print(response)
        if 'success' in response:
            response_value = response['success']
            response_value = f"Encontrei 3 vagas para você. Confira o conteúdo delas na sessão lateral da página. IDs: {response_value}"
            return response_value
        
        else:
            response_value = "☹️ Desculpe, infelizmente não consegui realizar a busca neste momento. Por favor tente mais tarde. \n Motivo: "
            response_value += response['error']
            print(type(response_value))
            return response_value            
    
    else:
        print("Erro: ", response.status_code)
        response_value = "☹️ Desculpe, infelizmente não consegui realizar a busca neste momento. Por favor tente mais tarde. \n Erro: "
        response_value += response.status_code
        return response_value



#-----------------------------------------------FUNÇÕES DE FILTROS----------------------------------------------------

# @st.cache_data
# def import_df(path):
#     df = pd.read_csv(path)
#     return df


def filtrar_df_vagas(df_vagas: pd.DataFrame, filtro_perfil: str, filtro_nivel: str, filtro_uf: str, filtro_empresa: str):

    #Filtro o dataframe de vagas
    df = df_vagas.copy()
    if filtro_perfil != 'Selecione':
        df = df[df['perfil_vaga'] == filtro_perfil]
    if filtro_nivel != 'Selecione':
        df = df[df['nivel_cargo'] == filtro_nivel]
    if filtro_uf != 'Selecione':
        df = df[df['estado'] == filtro_uf]
    if filtro_empresa != 'Selecione':
        df = df[df['empresa_contratante'] == filtro_empresa]
    return df




def filtrar_df_vagas_ternario(df_vagas: pd.DataFrame, filtro_nivel: str, filtro_uf: str, filtro_empresa: str):

    #Filtro o dataframe de vagas
    df = df_vagas.copy()
    if filtro_nivel != 'Selecione':
        df = df[df['nivel_cargo'] == filtro_nivel]
    if filtro_uf != 'Selecione':
        df = df[df['estado'] == filtro_uf]
    if filtro_empresa != 'Selecione':
        df = df[df['empresa_contratante'] == filtro_empresa]
    return df








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



def msg_wait_a_sec():
    time.sleep(1)
    response = random.choice(
        [
            "Ok, aguarde alguns segundos que irei buscar a vaga ideal.",
            "Ótimo! Vou procurar a vaga perfeita para você, um segundo.",
            "Aguarde um momento que irei olhar nos meus arquivos.",
            "Perfeito! Um segundo que vou achar as vagas ideais para você.",
            "Tenho a vaga perfeita nos meus arquivos! Um segundo que vou pegar ela para você.",
            "Entendido! Tenho exatamente o que você precisa. Aguarde um momento.",
            "Maravilha! Já sei o que você precisa. Vou buscar a vaga ideal para você.",
        ]
    )

    return response


def typing_effect(text):
    for phrase in text.split('\n'):
        time.sleep(1)
        for word in phrase.split():
            yield word + " "
            time.sleep(0.05)
        yield "  \n" 
#-----------------------------------------------FUNÇÕES DE GRÁFICOS----------------------------------------------------
