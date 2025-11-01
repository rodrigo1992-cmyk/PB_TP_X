import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv
from fastapi import HTTPException

def validar_input(input_sentence):
    '''
    Função que recebe a frase que o usuário inseriu no chat e chama o Gemini para validar se é um input válido para busca de vagas ou se é uma frase irrelevante.

    Args:
    input_sentence (str): Frase que o usuário inseriu no chat

    Returns:
    response_text (dict): Dicionário com a resposta do Gemini

    Raises:
    HTTPException: Error 500 - Se houver um erro ao chamar o Gemini para validar o input
    '''
    
    prompt = f"""
    Você é um mecanismo de busca de vagas de emprego. Sua tarefa é avaliar a [ENTRADA] do usuário e determinar se ela é uma solicitação válida para busca de emprego ou uma frase irrelevante, como uma saudação ou reclamação.

    Instruções:
    1. Receba a entrada do usuário, que pode ser uma descrição ou um conjunto de palavras.
    2. Avalie se a entrada é um input para busca de vagas de emprego.
    3. Se a entrada for um input válido para busca, responda apenas "input_valido".
    4. Se a entrada for um input inválido, responda de forma genérica utilizando um tom amigável, solicitando que o usuário forneça uma descrição adequada para a busca. Não repita o input do usuário na resposta.

    Exemplo de entradas válidas:
    "Bom dia! Gostaria de buscar uma vaga para cientista de dados"
    "Estou procurando oportunidades de trabalho como analista de dados."
    "Python, Matplotlib, Streamlit"
    "Uma vaga que tenha como requisitos Power BI, SQL e Excel"

    Exemplo de entradas inválidas:
    "Oi, tudo bem?"
    "Quero buscar uma vaga"
    "Não era bem isso que eu estava buscando"

    #[ENTRADA]#
    {input_sentence}
    """
    try:
        load_dotenv()
        key_gemini = os.getenv('GEMINI_KEY')

        genai.configure(api_key=key_gemini)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        response_text = response.text.replace('\n', '')

        if response_text == 'input_valido':
            return {"success": "input_valido"}
        else:
            return {"message": response_text}

        
    
    except: raise HTTPException(status_code=500, detail="⛔ Erro ao invocar o Gemini para validar o input")
    

def search_vagas(model_name, cache_file, db_path, input_sentence):
    '''
    Função que recebe a frase que o usuário inseriu no chat e chama o modelo de LLM para buscar a vaga mais similar.

    Args:
    model_name (str): Nome do modelo de LLM
    cache_file (str): Nome do arquivo de cache
    db_path (str): Caminho do arquivo csv com as vagas
    input_sentence (str): Frase que o usuário inseriu no chat

    Returns:
    dict_result (dict): Dicionário com a vaga encontrada

    Raises:
    HTTPException: Error 500 - Se houver um erro ao instanciar o SentenceTransformer
    HTTPException: Error 500 - Se houver um erro ao carregar o cache existente do modelo de LLM
    HTTPException: Error 500 - Se houver um erro ao criar o embeddings da base de dados
    HTTPException: Error 422 - Se houver um erro ao realizar o embedding do input_sentence
    HTTPException: Error 500 - Se houver um erro ao calcular as similaridades
    '''
    
    # Inicializar o modelo
    try: model = SentenceTransformer(model_name)
    except: raise HTTPException(status_code=500, detail="⛔ Erro ao instanciar o SentenceTransformer")

    # Verificar se o cache já existe
    if os.path.exists(cache_file):
        try: sentence_embeddings = np.load(cache_file)
        except: raise HTTPException(status_code=500, detail="⛔ Erro ao carregar o cache existente do modelo de LLM")
    
    else:
        try:
            df = pd.read_csv(db_path)

            #transformar em um dicionário com id_vaga e descricao
            df_embd = df[['id_vaga', 'descricao']].set_index('id_vaga').to_dict()['descricao']

            sentence_embeddings = model.encode(list(df_embd.values()))
            np.save(cache_file, sentence_embeddings)
        except:
            raise HTTPException(status_code=500, detail="⛔ Erro ao criar o embeddings da base de dados")


    # Codificar a frase de entrada (input)
    
    try: input_embedding = model.encode(input_sentence)
    except: raise HTTPException(status_code=422, detail="⛔ Erro ao realizar o embedding do input_sentence")

    # Calcular a similaridade entre a frase de entrada e o conjunto de dados
    try:
        similarities = util.cos_sim(input_embedding, sentence_embeddings).cpu().numpy().flatten()  # Garantir que seja um vetor 1D
    except:
        raise HTTPException(status_code=500, detail="⛔ Erro ao calcular as similaridades")

    index_vaga = np.argsort(similarities)[::-1][:1]

    index_vaga =  index_vaga.tolist()[0]

    with open(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X\app\data\processed\vagas_norm.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        dic_vagas = list(reader)

        dict_result = dic_vagas[index_vaga]

    return {'success': dict_result}


def formatar_output(output_content):
    '''
    Função que recebe a descrição da vaga e chama o Gemini para formatar o texto.

    Args:
    output_content (str): Descrição da vaga

    Returns:
    response (dict): Dicionário com a descrição da vaga formatada

    Raises:
    HTTPException: Error 500 - Se houver um erro ao invocar o Gemini para formatar a descrição da vaga
    '''
    
    prompt = f"""
    Por favor, organize e formate a [DESCRIÇÃO DA VAGA] a seguir em uma estrutura clara e legível. 
    Não crie nenhum texto, somente utilize o conteúdo da [DESCRIÇÃO DA VAGA]. 
    Corrija erros de pontuação e utilize Markdown para a formatação, garantindo que o texto seja fácil de ler e bem estruturado.
    Não adicione frases duplicadas. Se não houver conteúdo para um dos tópicos, não inclua a seção.
    
    UTILIZE A SEGUINTE ESTRUTURA:
    Sobre a Empresa: Escreva uma breve introdução sobre a empresa, somente se houver na descrição.
    Responsabilidades e Atribuições: Liste as principais responsabilidades da posição em formato de lista. São as funções e tarefas que o candidato irá desempenhar.
    Requisitos e Qualificações: Liste os requisitos e qualificações necessárias, também em formato de lista. São os hard-skills que o candidato deve possuir.
    Diferenciais: Inclua uma seção para diferenciais que podem ser considerados um plus para a vaga. São os hard-skills listados como desejáveis, ou soft-skills.
    
    EXEMPLO PARA FORMATAÇÃO EM MARKDOWN:
    ### Sobre a Empresa
    [Texto da descrição]

    ### Responsabilidades e Atribuições
    - [Responsabilidade 1]
    - [Responsabilidade 2]

    ### Requisitos e Qualificações
    - [Requisito 1]
    - [Requisito 2]

    ### Diferenciais
    - [Diferencial 1]
    - [Diferencial 2]
    

    DESCRIÇÃO DA VAGA:
    {output_content}
    """
    try:
        load_dotenv()
        key_gemini = os.getenv('GEMINI_KEY')

        genai.configure(api_key=key_gemini)
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        return {"success": response.text}
    except:
        raise HTTPException(status_code=500, detail="⛔ Erro ao invocar o Gemini para formatar a descrição da vaga")