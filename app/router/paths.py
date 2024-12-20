import sys
sys.path.append(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X')

import os
from fastapi import HTTPException, FastAPI
import csv
import json
import pandas as pd
from pydantic import ValidationError, field_validator, BaseModel
from typing import List
from fastapi.encoders import jsonable_encoder
from app.services.llm_search import *
from app.model.api_models import *



def dicionario_paths():
    '''
    Retorna um dicionário com os caminhos dos arquivos utilizados no projeto

    Returns:
    dic_paths (dict): Dicionário com os caminhos dos arquivos

    '''
    BASE_DIR = r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X'

    dic_paths = {
        'csv_links': os.path.join(BASE_DIR, r'app\data\raw\links_vagas_catho.csv'),
        'csv_links_indeed' : os.path.join(BASE_DIR, r'app\data\raw\links_vagas_indeed.csv'),
        'folder_htmls': os.path.join(BASE_DIR, r'app\data\html_pages'),
        'csv_vagas_catho': os.path.join(BASE_DIR, r'app\data\raw\vagas_catho.csv'),
        'csv_vagas_indeed' : os.path.join(BASE_DIR, r'app\data\raw\vagas_indeed.csv'),
        'csv_vagas': os.path.join(BASE_DIR, r'app\data\raw\vagas.csv'),
        'csv_vagas_norm': os.path.join(BASE_DIR, r'app\data\processed\vagas_norm.csv'),
        'csv_lista_ferramentas': os.path.join(BASE_DIR, r'app\data\processed\ferramentas.csv'),
        'csv_requisitos': os.path.join(BASE_DIR, r'app\data\processed\requisitos.csv')
    }
    return dic_paths

#------------------------Funções de API------------------------

dic_paths = dicionario_paths()
router = FastAPI()




@router.get("/csv_vagas_norm")
async def read_data_vagas_norm():

    '''
    Retorna o arquivo csv de vagas em um formato de lista de dicionários. Cada linha do CSV vira um dicionário.

    Returns:
    list_dict_resul (list): Lista de dicionários com as vagas
    '''
    with open(dic_paths['csv_vagas_norm'], mode='r', encoding='utf-8') as file:
        dados = csv.DictReader(file)

        # Validação com Pydantic descartando linhas com erro. (Tenta fazer a conversão, e usa o except para exibir os valores que não passaram na validação)
        dados_validados = []
        linha = 0
        for item in dados:
            linha += 1
            try: dados_validados.append(SchemaDFVagas(**item))
            except ValidationError as erro:
                log = erro.errors()[0]
                print('Erro na Linha:', linha, '| Coluna: ', log['loc'][0], '| Valor: ', log['input'], '| Tipo Esperado:', log['type'])

        #Remontando como uma lista de dicionários. Cada linha do CSV é um dicionário
        list_dict_resul = [item.model_dump() for item in dados_validados]

    return list_dict_resul



@router.get("/csv_requisitos")
async def read_data_requisitos():
    '''
    Retorna um arquivo com a relação de cada requisito (ferramenta) solicitado em cada vaga.
    Uma linha por requisito.

    Returns:
    data (list): Lista de dicionários com os requisitos
    '''

    with open(dic_paths['csv_requisitos'], mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        data = []
        for row in reader:
            try:
                # Valida os dados com o modelo Pydantic
                requisito = SchemaDFRequisito(id_vaga=row['id_vaga'], tool=row['tool'])
                # Adiciona ao resultado no formato original
                data.append(row)

            except ValidationError as erro:
                log = erro.errors()[0]
                print('Valor: ', log['input'], '| Tipo Esperado:', log['type'])

    return data 




@router.post("/api_post_new_vagas/")
async def api_post_new_vagas(novas_vagas: list[SchemaDFVagas]):
    '''
    Adiciona novas vagas ao arquivo csv_vagas_norm.

    Args:
    novas_vagas (list): Lista de dicionários com as novas vagas a serem adicionadas.

    Returns:
    response (str): Mensagem de sucesso ou erro

    Raises:
    HTTPException: Error 400 - Se uma ou mais vagas carregadas já estão contidas no dataframe atual.
    HTTPException: Error 400 - Se há ids duplicados nas vagas carregadas.

    Example:
    [
        {
            "id_vaga": "30077919",
            "data_anuncio": "2024-08-16T23:59:59Z",
            "titulo_vaga": "Analista de Dados - Júnior",
            "titulo_resumo": "analista-de-dados-junior",
            "faixa_salarial": "não disponível",
            "empresa_contratante": "CARTÃO DE TODOS",
            "estado": "MG",
            "cidade": "Ipatinga",
            "url": "/vagas/analista-de-dados-junior/30077919/",
            "descricao": "Exemplo Descrição",
            "beneficios": ['Seguro Saúde', 'Assistência Médica / Medicina em grupo'],
            "regimeContrato": "CLT (Efetivo)"
        },
        {
            "id_vaga": "30045699",
            "data_anuncio": "2024-08-21T23:59:59Z",
            "titulo_vaga": "Cientista de Dados Sênior",
            "titulo_resumo": "cientista-de-dados-senior",
            "faixa_salarial": "não disponível",
            "empresa_contratante": "DECISION",
            "estado": "SP",
            "cidade": "São Paulo",
            "url": "/vagas/cientista-de-dados-senior/30045699/",
            "descricao": "Exemplo Descrição",
            "beneficios": [],
            "regimeContrato": ""
        }
    ]
    '''

    df_vagas = pd.read_csv(dic_paths['csv_vagas_norm'])
    
    #Esse passo foi muito importante para conseguir converter o que foi recebido pela API em Json e depois para DF 
    novas_vagas_json = jsonable_encoder(novas_vagas)
    df_novas_vagas = pd.DataFrame(novas_vagas_json)

    #Conferir se o id_vaga já existe
    if df_novas_vagas['id_vaga'].isin(df_vagas['id_vaga']).any():
        raise HTTPException(status_code=400, detail="Uma ou mais das vagas carregadas já estão contidas no dataframe atual.")
    
    #Conferir se há ids duplicados
    if df_novas_vagas['id_vaga'].duplicated().any():
        raise HTTPException(status_code=400, detail="Há ids duplicados nas vagas carregadas.")
    
    else:
        df = pd.concat([df_vagas, df_novas_vagas], ignore_index=True)
        df.to_csv(dic_paths['csv_vagas_norm'], index=False)
        response = "Vagas adicionadas com sucesso!"

        return {response}




@router.post("/api_llm_search/")
async def api_post_llm_search(input_sentence: ApiLlmSearchInput):
    '''
    Função que recebe a frase que o usuário inseriu no chat e trata em 3 etapas:
    1. Chama o Gemini para validar o input
    2. Chama o Mpnet para buscar a vaga
    3. Chama o Gemini para formatar o resultado

    Args:
    input_sentence (str): Frase que o usuário inseriu no chat

    Returns:
    response_search (dict): Dicionário com a vaga encontrada

    Raises:
    HTTPException: Error 500 - Se houver um erro ao chamar o Gemini para validar o input
    HTTPException: Error 500 - Se houver um erro ao chamar o Mpnet para buscar a vaga
        Dentro da função search_vagas:
        HTTPException: Error 500 - Se houver um erro ao instanciar o SentenceTransformer
        HTTPException: Error 500 - Se houver um erro ao carregar o cache existente do modelo de LLM
        HTTPException: Error 500 - Se houver um erro ao criar o embeddings da base de dados
        HTTPException: Error 422 - Se houver um erro ao realizar o embedding do input_sentence
        HTTPException: Error 500 - Se houver um erro ao calcular as similaridades
    HTTPException: Error 500 - Se houver um erro ao chamar o Gemini para formatar o resultado
    '''

    #Chama o Gemini para validar o input
    print('Input recebido, chamando Gemini para validar')
    response_gemini = validar_input(input_sentence)

    
    if 'message' in response_gemini:
        #Neste caso o Gemini vai pedir para que o usuário descreva a vaga
        return response_gemini

    elif response_gemini.get('success') == 'input_valido':
        #Chama o Mpnet para buscar a vaga
        print('Input validado, chamando Mpnet para buscar a vaga')    
        response_search = search_vagas(
            model_name = "sentence-transformers/all-mpnet-base-v2", 
            cache_file = "embeddings_cache3.npy", 
            db_path = dic_paths['csv_vagas_norm'],
            input_sentence = input_sentence.text
        )
        
        #Chama o Gemini par formatar o resultado
        if 'success' in response_search:

            print('Vaga localizada, chamando Gemini para formatar resultado')    
            description_format = formatar_output(response_search['success']['descricao'])
            
            if 'success' in description_format:
                response_search['success']['descricao'] = description_format['success']

                print('Resultado formatado, será enviado via API')  
                print(response_search)  
                return response_search
            
