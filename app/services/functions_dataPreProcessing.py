

import pandas as pd
import re

def Pre_Processamento_Df_Vagas(path_csv_vagas, path_csv_vagas_norm):
    df_vagas = pd.read_csv(path_csv_vagas)
    df_vagas['empresa_contratante'] = df_vagas['empresa_contratante'].str.upper()
    df_vagas['empresa_contratante'] = df_vagas['empresa_contratante'].replace('CLIENTE', 'EMPRESA CONFIDENCIAL').replace('CONFIDENCIAL', 'EMPRESA CONFIDENCIAL').replace('********', 'EMPRESA CONFIDENCIAL')

    df_vagas['data_anuncio'] = pd.to_datetime(df_vagas['data_anuncio']).dt.date

    #Adicionar uma coluna de região (Sul, Sudeste, Centro-Oeste, Nordeste, Norte) a partir da coluna de estado
    df_vagas['regiao'] = df_vagas['estado'].map({'AC': 'Norte', 'AL': 'Nordeste', 'AP': 'Norte', 'AM': 'Norte', 'BA': 'Nordeste', 'CE': 'Nordeste', 'DF': 'Centro-Oeste', 'ES': 'Sudeste', 'GO': 'Centro-Oeste', 'MA': 'Nordeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'MG': 'Sudeste', 'PA': 'Norte', 'PB': 'Nordeste', 'PR': 'Sul', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RJ': 'Sudeste', 'RN': 'Nordeste', 'RS': 'Sul', 'RO': 'Norte', 'RR': 'Norte', 'SC': 'Sul', 'SP': 'Sudeste', 'SE': 'Nordeste', 'TO': 'Norte'})




    #----------- Classificar as vagas nas categorias: Analista, Cientista ou Engenheiro de Dados------------
    lista_vagas = df_vagas.titulo_resumo.unique()

    de_para_vagas = {}

    for vaga in lista_vagas:
        if 'eng' in vaga and 'dados' in vaga:
            norm = 'engenheiro'
        elif 'anal' in vaga and 'dados' in vaga:
            norm = 'analista'
        elif 'cientista' in vaga or 'ciencia' in vaga:
            norm = 'cientista'
        elif 'anal' in vaga and 'bi' in vaga:
            norm = 'analista'
        elif 'intell' in vaga:
            norm = 'analista'        
        else:
            norm = 'outros'

        de_para_vagas[vaga] = norm

    #Join para trazer a classificação das vagas
    df_vagas['perfil_vaga'] = df_vagas['titulo_resumo'].map(de_para_vagas)

    #Retirar  as duas vagas que ficaram como "outros", pois eram de analistas de sistemas
    df_vagas = df_vagas[df_vagas['perfil_vaga'] != 'outros']





    #-----------Descobrindo a Serionidade da Vaga (Junior, Pleno, Senior)------------

    lista_vagas = df_vagas.titulo_resumo.unique()

    nivel_cargo = {}

    for vaga in lista_vagas:
        if 'senior' in vaga or 'sr' in vaga:
            nivel = 'senior'
        elif 'junior' in vaga or 'jr' in vaga:
            nivel = 'junior'   
        else:
            nivel = 'pleno'

        nivel_cargo[vaga] = nivel

    #Join para trazer a classificação das vagas
    df_vagas['nivel_cargo'] = df_vagas['titulo_resumo'].map(nivel_cargo)



    #--------------Ajustando a média salarial a partir da faixa salarial---------------------

    for i,row in df_vagas.iterrows():
        if pd.isnull(row.faixa_salarial):
            row.salario = None
        else:
            pattern = r"R\$ ([\d\.]+,\d{2}) a R\$ ([\d\.]+,\d{2})"
            match = re.search(pattern, row.faixa_salarial)
            if match:
                minimo = float(match.group(1).replace('.','').replace(',','.'))
                maximo = float(match.group(2).replace('.','').replace(',','.'))
                media = round((minimo + maximo) / 2, 0)
            else:
                media = None

            df_vagas.at[i, 'salario'] = media


    df_vagas.to_csv(path_csv_vagas_norm, index=False)




#-----------------------------Buscando os requisitos ferramentais em cada vaga-----------------------------
def Pre_Processamento_Df_Requisitos(path_csv_lista_ferramentas, path_csv_vagas, path_csv_requisitos):

    df_vagas = pd.read_csv(path_csv_vagas)
    df_lista_ferramentas = pd.read_csv(path_csv_lista_ferramentas)
    conjunto_tools = set(df_lista_ferramentas['FERRAMENTAS'].str.upper())
    requisitos = []

    for i, row in df_vagas.iterrows():
        #remover pontuações do campo de descrição
        descricao = row['descricao'].replace(',', ' ').replace('.', ' ').replace(';', ' ').replace(':', ' ').replace('(', ' ').replace(')', ' ')
        
        #transformar a descrição em uma conjunto de palavras
        desc = descricao.upper().split()
        conjunto_desc = set(desc)

        #verificar a intersecção entre as palavras da descrição e as palavras do conjunto de ferramentas
        interseccao = conjunto_desc.intersection(conjunto_tools)

        #converter a interseccao em uma lista
        lista_interseccao = list(interseccao)

        #criar uma lista de tuplas com o id da vaga e a ferramenta
        for tool in lista_interseccao:
            id_vaga = row['id_vaga']
            requisitos.append([id_vaga, tool])

    df_requisitos = pd.DataFrame(requisitos, columns=['id_vaga', 'tool'])
    df_requisitos.to_csv(path_csv_requisitos)
