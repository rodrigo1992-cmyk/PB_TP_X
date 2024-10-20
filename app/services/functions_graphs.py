
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import nbformat 

def plot_hist_vagas(df):
    '''
    Função para plotar histórico de vagas publicadas por semana
    '''
    df['semana_anuncio'] = pd.to_datetime(df['data_anuncio']).dt.isocalendar()['week']

    df = df.groupby(['semana_anuncio', 'perfil_vaga']).agg({'perfil_vaga': 'count'}).rename(columns={'perfil_vaga': 'count'}).reset_index()

    fig = px.line(df, x='semana_anuncio', y='count', color='perfil_vaga', 
                title='Número de vagas por perfil profissional',
                markers=True)

    fig.show()

def plot_box_salarios(df):
    df = df[df['salario'].notna()]

    fig = px.box(df, y="salario", x="perfil_vaga")
    fig.update_traces(quartilemethod="inclusive")
    fig.update_layout(title='Distribuição de salários por perfil profissional')
    fig.show()

def plot_sun_salarios(df):
    df = df[df['salario'].notna()]

    fig = px.sunburst(df, path=['perfil_vaga', 'salario'], values='salario')
    fig.update_layout(title='Distribuição de salários por perfil profissional')
    fig.show()

def plot_dist_regiao(df):
    df = df.groupby(['regiao', 'perfil_vaga']).agg({'perfil_vaga': 'count'}).rename(columns={'perfil_vaga': 'count'}).reset_index()

    fig = px.sunburst(df, path=['perfil_vaga', 'regiao'], values='count')
    fig.update_layout(title='Número de vagas por perfil profissional e região')
    fig.show()
