import streamlit as st
import pandas as pd
import requests
import time
import random
import csv
import io

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

        return df
    else:
        st.error("Erro ao acessar a API: {}".format(response.status_code))




def control0():
    if 'control' in st.session_state:
        del st.session_state.control
        st.write('executou, sem control no ststate')
    if 'file_uploader' in st.session_state:
        del st.session_state['file_uploader']
        st.write('executou, o control está no ststate')
    st.rerun()


def api_post_new_vagas(uploaded_file):

    if uploaded_file is not None:

        #converter o csv em dicionário
        uploaded_file = io.TextIOWrapper(uploaded_file, encoding='utf-8')
        reader = csv.DictReader(uploaded_file)
        uploaded_dict = [row for row in reader]

        
        # No Json os valores em branco devem ser convertidos para None (Em campos de String) e para Zero (em campos numéricos)
        # A função abaixo faz essa conversão para os campos de string
        processed_strings_fields = [
            {key: (value if value != '' else None) for key, value in row.items()}
            for row in uploaded_dict
        ]

        # A função abaixo faz essa conversão para os campos de numéricos (apenas o campo salario)
        processed_number_fields = [
            {key: (0 if key == "salario" and value is None else value) for key, value in row.items()}
            for row in processed_strings_fields
        ]

        processed_dict = processed_number_fields

        st.write('### Pré-Visualização das linhas a serem carregadas')
        st.dataframe(processed_dict, height = 200)

        if st.button("Confirmar Upload", icon="✅"):
            try:
                response = requests.post("http://localhost:8000/api_post_new_vagas", json=processed_dict)
                response.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx

                st.session_state.df_vagas = api_get_file_vagas_norm()
                
                st.success("Upload Concluído com Sucesso.")
                time.sleep(4)
                control0()

            except requests.exceptions.HTTPError as http_err:
                # Captura o erro e exibe a mensagem de detalhe
                st.error(f"Erro: {http_err}", icon="🚨")


def api_post_llm_search(search_sentence):

    dict = {'text': search_sentence}
    print("Input convertido em dict, será realizado o request")

    response = requests.post("http://localhost:8000/api_llm_search", json=dict)
    
    if response.status_code == 200:
        print("Resposta recebida com sucesso")

        response = response.json()

        print(response)
        if 'success' in response:
            lista_ids = response['success']
            response_value = "Encontrei 3 vagas para você. Dá uma olhada"
            return response_value, lista_ids
        
        else:
            response_value = "☹️ Desculpe, infelizmente não consegui realizar a busca neste momento. Por favor tente mais tarde. \n Motivo: "
            response_value += response['error']
            print(type(response_value))
            lista_ids = ['']
            return response_value, lista_ids     
    
    else:
        print("Erro: ", response.status_code)
        response_value = "☹️ Desculpe, infelizmente não consegui realizar a busca neste momento. Por favor tente mais tarde. \n Erro: "
        response_value += response.status_code
        lista_ids = ['']
        return response_value, lista_ids


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
        time.sleep(0.1)
        for word in phrase.split():
            yield word + " "
            time.sleep(0.02)
        yield "  \n" 

def buscar_id_na_base(lista_ids):

    df_vagas = st.session_state.df_vagas

    df_ids = pd.DataFrame(lista_ids, columns=['id_vaga'], dtype='string')

    df = pd.merge(df_ids, df_vagas, on='id_vaga', how='left')
    texto = ''

    for _, row in df.iterrows():
        texto += f'''
            {row['titulo_vaga']}
            Perfil: {row['perfil_vaga']}-{row['nivel_cargo']}
            Empresa: {row['empresa_contratante']}
            Local: {row['cidade']} - {row['estado']}
            Anunciada em: {row['data_anuncio']}
            Disponível no link: {row['url']}
            Descrição: {row['descricao']}


        '''

    return texto
