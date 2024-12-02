import streamlit as st
import pandas as pd
import requests
import time
import random
import csv
import io
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import nbformat 
from wordcloud import WordCloud
from collections import Counter
import json

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
                
                #Dá um refresh na base df_vagas que estava no session_state, para que apareçam as novas vagas carregadas
                st.session_state.df_vagas = api_get_file_vagas_norm()
                
                st.success("Upload Concluído com Sucesso.")
                time.sleep(4)
                control0()

            except requests.exceptions.HTTPError as http_err:
                # Captura o erro e exibe a mensagem de detalhe
                st.error(f"Erro: {http_err}", icon="🚨")




def api_post_llm_search(search_sentence):
    dict_sentence = {'text': search_sentence}

    print("Será feito o request à API")
    response = requests.post("http://localhost:8000/api_llm_search", json=dict_sentence)
    print("Resposta recebida")

    if response.status_code == 200:
        content = response.json()
        if 'success' in content:
            y = content['success']
            content_str = f"""
## {y['titulo_vaga']}  \n
**Empresa:** {y['empresa_contratante']} | **Local:** {y['cidade']} - {y['estado']} | **Anunciada em:** {y['data_anuncio']} | **Disponível em:** [link]({y['url']})  \n
{y['descricao']}
            """

            return content_str



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



def typing_effect(text):
    for phrase in text.split('\n'):
        time.sleep(0.1)
        for word in phrase.split():
            yield word + " "
            time.sleep(0.02)
        yield "  \n" 


#-----------------------------------------------CRIAÇÃO DE GRÁFICOS----------------------------------------------------

def plot_historico_vagas(df):
    '''
    Função para plotar histórico de vagas publicadas por semana
    args:
        df: usar o dataframe vagas_norm
    '''


    df['semana_anuncio'] = pd.to_datetime(df['data_anuncio']).dt.isocalendar()['week']

    df = df.groupby(['semana_anuncio', 'perfil_vaga']).agg({'perfil_vaga': 'count'}).rename(columns={'perfil_vaga': 'count'}).reset_index()

    df_filt = df[(df['semana_anuncio'] >= 25) & (df['semana_anuncio'] <= 43)]

    fig = px.line(df_filt, x='semana_anuncio', y='count', color='perfil_vaga',
                markers=True)

    st.plotly_chart(fig)


def plot_box_salarios(df):
    '''
    args:
        df: usar o dataframe vagas_norm
    '''

    df_filt = df[df['salario'] != 0]

    color_palette = ['#0068C9', '#83C9FF', '#FF2B2B']

    fig = px.box(df_filt, y="salario", x="perfil_vaga", color="perfil_vaga",color_discrete_sequence=color_palette)
    fig.update_traces(quartilemethod="inclusive")
    
    st.plotly_chart(fig)

def plot_dist_senioridade(df):
    '''
    args:
        df: usar o dataframe vagas_norm
    '''
    df = df.groupby(['perfil_vaga', 'nivel_cargo']).agg(count=('salario', 'size'), media_salario=('salario', 'mean')).reset_index()
    #converter a média salarial para int, exceto o que for nan
    df['media_salario'] = df['media_salario'].apply(lambda x: int(x) if not np.isnan(x) else x)

    #plotando o gráfico
    fig = px.sunburst(df, path=['perfil_vaga', 'nivel_cargo'], values='count',
                    color='media_salario',
                    color_continuous_scale='PuBu',)
    fig.update_traces(textinfo='label+percent parent')
    st.plotly_chart(fig)

def plot_dist_regiao(df):
    '''
    args:
        df: usar o dataframe vagas_norm
    '''
    df = df[df['estado'] != 'N/I']

    df = df.groupby(['perfil_vaga','regiao', 'estado']).size().reset_index(name='count')

    fig = px.sunburst(df, path=['perfil_vaga', 'regiao', 'estado'], values='count')
    fig.update_traces(textinfo='label+percent parent')
    st.plotly_chart(fig)

def plot_wordcloud(df):
    '''
    Função para plotar um wordcloud com as palavras mais frequentes
    args:
        df: usar o dataframe requisitos
    '''
    df = df.groupby(['tool']).size().reset_index(name='count')

    word_freq = dict(zip(df['tool'], df['count']))

    # Criar o wordcloud
    wc = WordCloud(width=800, height=400, max_words=200, background_color='white').generate_from_frequencies(word_freq)

    # Plotar o wordcloud
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(plt)


def plot_ternario_requisitos(df_vagas_completo, df_ternario_filt, df_reqs):
    '''
    Função para plotar um gráfico ternário com os requisitos de ferramentas por perfil profissional
    args:
        df_vagas_completo: usar o dataframe vagas_norm completo (sem filtros palicados), para que possa checar se no filtro algum perfil não tem dados
        df_ternario_filt: usar o dataframe vagas_norm filtrado pela função filtrar_df_vagas_ternario, que não aplica filtro de perfil
        df_reqs: usar o dataframe requisitos
    '''

    lista_perfis = df_vagas_completo['perfil_vaga'].unique()
    check_filtro = 0

    for perfil in lista_perfis:
        if df_ternario_filt[df_ternario_filt['perfil_vaga'] == perfil].empty:
            check_filtro += 1

    if check_filtro > 0:
        st.error('Não há dados suficientes para comparação no Diagrama de Ternário. Ajuste as seleções de filtro.', icon = "🚨")

    else:
        # Fazer um left join entre os dataframes
        df_ternario_filt = df_ternario_filt[['id_vaga', 'perfil_vaga']]
        df = pd.merge(df_ternario_filt, df_reqs, on='id_vaga', how='left')

        # Contar o uso de cada ferramenta por perfil
        df_counts = df.groupby(['perfil_vaga', 'tool']).size().reset_index(name='count')

        # Limitei apenas às ferramentas que aparecem em pelo menos 3 vagas, pois o gráfico estava muito poluído
        df_counts = df_counts[df_counts['count'] > 2]

        # Pivotar o DataFrame para ter perfis como colunas
        df_pivot = df_counts.pivot(index='tool', columns='perfil_vaga', values='count').fillna(0)

        # Calcular a contagem total de linhas para cada perfil
        total_counts = df.groupby('perfil_vaga').size()

        # Normalizar as contagens pela quantidade total de cada perfil
        for perfil in total_counts.index:
            if perfil in df_pivot.columns:
                df_pivot[perfil] = df_pivot[perfil] / total_counts[perfil]

        # Adicionar um pequeno valor constante para empurrar os pontos para o centro
        epsilon = 0.003  # Valor pequeno
        for perfil in total_counts.index:
            if perfil in df_pivot.columns:
                df_pivot[perfil] += epsilon


        # Adicionar uma coluna com o perfil mais frequente
        df_pivot['winner'] = df_pivot.idxmax(axis=1)

        # Adicionar coluna somando os campos analista, cientista e engenheiro
        df_pivot['total'] = df_pivot['analista'] + df_pivot['cientista'] + df_pivot['engenheiro']

        df_pivot.reset_index(inplace=True)

        # Criar o gráfico ternário
        fig = px.scatter_ternary(df_pivot, 
                                a='cientista', 
                                b='analista', 
                                c='engenheiro', 
                                hover_name='tool',
                                color="winner", 
                                size="total", 
                                size_max=30,
                                text='tool'  # Adiciona rótulos diretamente
                                )

        #ajustar o máximo dos eixos
        fig.update_ternaries(aaxis_min=0, baxis_min=0, caxis_min=0)

        # Atualizar o layout para melhorar a visualização
        fig.update_traces(textposition='top center', 
                        textfont=dict(size=9))  # Ajusta o tamanho da fonte das anotações

        fig.update_layout(height=1000, width=1382)

        # Exibir o gráfico
        st.plotly_chart(fig)


def top_requisitos(df_vagas, df_reqs):

    #Junta os dois dataframes para trazer o perfil da vaga (necessário para usar nos filtros futuramente)
    df_vagas = df_vagas[['id_vaga', 'perfil_vaga']]
    df = pd.merge(df_vagas, df_reqs, on='id_vaga', how='left')

    # Contar o número total de vagas
    n_vagas_total = df['id_vaga'].nunique()

    # Agrupar por ferramenta e calcular percentuais
    df_grouped = df.groupby('tool')['id_vaga'].nunique().reset_index(name='n_vagas_requisito')
    df_grouped['perc_tool'] = df_grouped['n_vagas_requisito'] / n_vagas_total
    df_grouped['delta'] = 1 - df_grouped['perc_tool']

    # Filtrar as 10 ferramentas mais solicitadas
    df_top10 = df_grouped.nlargest(10, 'n_vagas_requisito')

    # Criar gráfico de barras empilhadas
    fig = go.Figure()

    # Adicionar barra para perc_tool
    fig.add_trace(go.Bar(
        x=df_top10['tool'],
        y=df_top10['perc_tool'],
        name='% solicitação',
        text=[f'{p:.0%}' for p in df_top10['perc_tool']],
        textposition='inside',
        insidetextanchor='middle',
        marker_color='blue'
    ))

    # Adicionar barra para delta
    fig.add_trace(go.Bar(
        x=df_top10['tool'],
        y=df_top10['delta'],
        name='delta',
        text=[f'{d:.0%}' for d in df_top10['delta']],
        textposition='inside',
        insidetextanchor='middle',
        marker_color='lightgrey'
    ))

    # Ajustar layout
    fig.update_layout(
        yaxis_title='Percentual de vagas (%)',
        barmode='stack',
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig)