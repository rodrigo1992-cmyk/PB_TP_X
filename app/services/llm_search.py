import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import os


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

    posicao_top_3 = np.argsort(similarities)[::-1][:3]

    top_3_id_vaga = df.iloc[posicao_top_3]["id_vaga"]  # Selecionar as linhas correspondentes aos índices do embedding

    response = top_3_id_vaga.tolist()

    return {"success": response}