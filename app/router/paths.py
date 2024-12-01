import sys
sys.path.append(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X')

import os
from fastapi import APIRouter, HTTPException
import csv
import json
import pandas as pd
from pydantic import ValidationError, field_validator, BaseModel
from typing import List
from fastapi.encoders import jsonable_encoder
from app.services.llm_search import search_vagas
from app.model.api_models import *



def dicionario_paths():
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
router = APIRouter()





@router.get("/csv_vagas_norm")
async def read_data_vagas_norm():
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





# @router.get("/csv_requisitos")
# async def read_data_requisitos():
#     with open(dic_paths['csv_requisitos'], mode='r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         data = [row for row in reader]  

#     return data 




@router.get("/csv_requisitos")
async def read_data_requisitos():
    with open(dic_paths['csv_requisitos'], mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        data = []
        for row in reader:
            try:
                # Valida os dados com o modelo Pydantic
                requisito = SchemaDFRequisito(id_vaga=int(row['id_vaga']), tool=row['tool'])
                # Adiciona ao resultado no formato original
                data.append(row)

            except ValidationError as erro:
                log = erro.errors()[0]
                print('Valor: ', log['input'], '| Tipo Esperado:', log['type'])

    return data 




@router.post("/api_post_new_vagas/")
async def api_post_new_vagas(novas_vagas: list[SchemaDFVagas]):

    df_vagas = pd.read_csv(dic_paths['csv_vagas_norm'])
    
    #Esse passo foi muito importante para conseguir converter o que foi recebido pela API em Json e depois para DF 
    novas_vagas_json = jsonable_encoder(novas_vagas)
    df_novas_vagas = pd.DataFrame(novas_vagas_json)

    #Conferir se o id_vaga já existe
    if df_novas_vagas['id_vaga'].isin(df_vagas['id_vaga']).any():
        raise HTTPException(status_code=400, detail="Uma ou mais das vagas carregadas já estão contidas no dataframe atual.")
    
    else:
        df = pd.concat([df_vagas, df_novas_vagas], ignore_index=True)
        df.to_csv(dic_paths['csv_vagas_norm'], index=False)
        response = "Vagas adicionadas com sucesso!"

        return {response}



@router.post("/api_llm_search/")
async def api_post_llm_search(input_sentence: ApiLlmSearchInput):

    print("Input recebido, formato válido. Invocando a função de busca...")

    try:
        #chamar o modelo
        result = search_vagas(
            model_name = "sentence-transformers/all-mpnet-base-v2", 
            cache_file = "embeddings_cache3.npy", 
            db_path = dic_paths['csv_vagas_norm'],
            input_sentence = input_sentence.text
        )

        return result
    
    except Exception as e:
        return {"error": str(e)}