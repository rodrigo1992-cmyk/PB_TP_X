
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import nbformat 
from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt

def plot_historico_vagas(df):
    '''
    Função para plotar histórico de vagas publicadas por semana
    args:
        df: usar o dataframe vagas_norm
    '''
    df['semana_anuncio'] = pd.to_datetime(df['data_anuncio']).dt.isocalendar()['week']

    df = df.groupby(['semana_anuncio', 'perfil_vaga']).agg({'perfil_vaga': 'count'}).rename(columns={'perfil_vaga': 'count'}).reset_index()

    fig = px.line(df, x='semana_anuncio', y='count', color='perfil_vaga',
                markers=True)

    st.plotly_chart(fig)

def plot_box_salarios(df):
    '''
    args:
        df: usar o dataframe vagas_norm
    '''

    df = df[df['salario'].notna()]

    color_palette = ['#0068C9', '#83C9FF', '#FF2B2B']

    fig = px.box(df, y="salario", x="perfil_vaga", color="perfil_vaga",color_discrete_sequence=color_palette)
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