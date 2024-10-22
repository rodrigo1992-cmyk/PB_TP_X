import os
from fastapi import APIRouter, HTTPException
import csv
import json

def dicionario_paths():
    BASE_DIR = r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X'

    dic_paths = {
        'csv_links': os.path.join(BASE_DIR, r'app\data\raw\links_vagas.csv'),
        'folder_htmls': os.path.join(BASE_DIR, r'app\data\html_pages'),
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
async def read_data():
    with open(dic_paths['csv_vagas_norm'], mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]  

    return data 

@router.get("/csv_requisitos")
async def read_data():
    with open(dic_paths['csv_requisitos'], mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]  

    return data 