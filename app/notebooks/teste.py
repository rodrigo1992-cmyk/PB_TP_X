import sys
sys.path.append(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X')

import os
from typing import List
from fastapi.encoders import jsonable_encoder
from app.services.llm_search import search_vagas
from app.model.api_models import *
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util

    
def search_vagas(model_name, cache_file, db_path, input_sentence): 

    df = pd.read_csv(db_path)

    # Inicializar o modelo
    try: model = SentenceTransformer(model_name)
    except: {"error": "⛔ Erro ao instanciar o modelo"}

    # Verificar se o cache já existe
    if os.path.exists(cache_file):
        try: sentence_embeddings = np.load(cache_file)
        except: return {"error": "⛔ Erro ao carregar o cache existente do modelo de LLM."}

    else:
        try:
            #transformar em um dicionário com id_vaga e descricao
            df = df[['id_vaga', 'descricao']].set_index('id_vaga').to_dict()['descricao']

            sentence_embeddings = model.encode(list(df.values()))
            np.save(cache_file, sentence_embeddings)
        except: return {"error": "⛔ Erro ao criar o embeddings da base de dados"}


    # Codificar a frase de entrada (input)
    
    try: input_embedding = model.encode(input_sentence)
    except: return {"error": "⛔ Erro ao realizar o embedding do input_sentence"}

    # Calcular a similaridade entre a frase de entrada e o conjunto de dados
    try:
        similarities = util.cos_sim(input_embedding, sentence_embeddings).cpu().numpy().flatten()  # Garantir que seja um vetor 1D
    except: return {"error": "⛔ Erro ao calcular as similaridades"}

    top_3_index = np.argsort(similarities)[::-1][:3]

    top_3_id_vaga = df.iloc[top_3_index]["id_vaga"]  # Selecionar as linhas correspondentes aos índices
    response = top_3_id_vaga.tolist()

    print(response)

    return {"success": response}

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

result = search_vagas(
    model_name = "sentence-transformers/all-mpnet-base-v2", 
    cache_file = "embeddings_cache3.npy", 
    db_path = dic_paths['csv_vagas_norm'],
    input_sentence = 'Analista de Dados, Power BI'
)

print(result)
