import os
from fastapi import APIRouter, HTTPException
import csv
import json
import pandas as pd
from pydantic import BaseModel 
from typing import List
from fastapi.encoders import jsonable_encoder


def dicionario_paths():
    BASE_DIR = r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X'

    dic_paths = {
        'csv_links': os.path.join(BASE_DIR, r'app\data\raw\links_vagas.csv'),
        'folder_htmls': os.path.join(BASE_DIR, r'app\data\html_pages'),
        'csv_vagas': os.path.join(BASE_DIR, r'app\data\raw\vagas.csv'),
        'csv_vagas_norm': os.path.join(BASE_DIR, r'app\data\processed\vagas_norm.csv'),
        'csv_lista_ferramentas': os.path.join(BASE_DIR, r'app\data\processed\ferramentas.csv'),
        'csv_requisitos': os.path.join(BASE_DIR, r'app\data\processed\requisitos.csv'),
        'csv_links_indeed' : os.path.join(BASE_DIR, r'app\data\raw\links_vagas_indeed.csv'),
        'csv_resultado_indeed' : os.path.join(BASE_DIR, r'app\data\raw\vagas_indeed.csv')
    }
    return dic_paths

#------------------------Funções de API------------------------

dic_paths = dicionario_paths()
router = APIRouter()





@router.get("/csv_vagas_norm")
async def read_data_vagas_norm():
    with open(dic_paths['csv_vagas_norm'], mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]  

    return data 





@router.get("/csv_requisitos")
async def read_data_requisitos():
    with open(dic_paths['csv_requisitos'], mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]  

    return data 


class Vaga(BaseModel):
    id_vaga: int
    data_anuncio: str
    titulo_vaga: str
    titulo_resumo: str
    faixa_salarial: str
    empresa_contratante: str
    estado:str
    cidade: str 
    url: str
    descricao: str
    beneficios: str
    regimeContrato: str
    regiao: str
    perfil_vaga: str
    nivel_cargo: str
    salario: int

@router.post("/api_post_new_vagas/")
async def api_post_new_vagas(novas_vagas: list[Vaga]):

    df_vagas = pd.read_csv(dic_paths['csv_vagas_norm'])
    
    #Esse passo foi muito importante para conseguir converter o que foi recebido pela API em Json e depois para DF 
    novas_vagas_json = jsonable_encoder(novas_vagas)
    df_novas_vagas = pd.DataFrame(novas_vagas_json)

        #Conferir se o id_vaga já existe
    if df_novas_vagas['id_vaga'].isin(df_vagas['id_vaga']).any():
        raise HTTPException(status_code=400, detail="Uma ou mais das vagas carregadas já estão contidas no dataframe atual.")
    
    
    df = pd.concat([df_vagas, df_novas_vagas], ignore_index=True)
    df.to_csv(dic_paths['csv_vagas_norm'], index=False)
    response = "Vagas adicionadas com sucesso!"

    return{response}