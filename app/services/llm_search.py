import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import os
import google.generativeai as genai
from dotenv import load_dotenv
import csv
    
def validar_input(input_sentence):
    
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
    load_dotenv()
    key_gemini = os.getenv('GEMINI_KEY')

    genai.configure(api_key=key_gemini)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    response_text = response.text.replace('\n', '')

    return {"success": response_text}


def search_vagas(model_name, cache_file, db_path, input_sentence):     
    
    # Inicializar o modelo
    try: model = SentenceTransformer(model_name)
    except: {"error": "⛔ Erro ao instanciar o modelo"}

    # Verificar se o cache já existe
    if os.path.exists(cache_file):
        try: sentence_embeddings = np.load(cache_file)
        except: return {"error": "⛔ Erro ao carregar o cache existente do modelo de LLM."}

    else:
        try:
            df = pd.read_csv(db_path)

            #transformar em um dicionário com id_vaga e descricao
            df_embd = df[['id_vaga', 'descricao']].set_index('id_vaga').to_dict()['descricao']

            sentence_embeddings = model.encode(list(df_embd.values()))
            np.save(cache_file, sentence_embeddings)
        except: return {"error": "⛔ Erro ao criar o embeddings da base de dados"}


    # Codificar a frase de entrada (input)
    
    try: input_embedding = model.encode(input_sentence)
    except: return {"error": "⛔ Erro ao realizar o embedding do input_sentence"}

    # Calcular a similaridade entre a frase de entrada e o conjunto de dados
    try:
        similarities = util.cos_sim(input_embedding, sentence_embeddings).cpu().numpy().flatten()  # Garantir que seja um vetor 1D
    except: return {"error": "⛔ Erro ao calcular as similaridades"}

    index_vaga = np.argsort(similarities)[::-1][:1]

    index_vaga =  index_vaga.tolist()[0]

    with open(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X\app\data\processed\vagas_norm.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        dic_vagas = list(reader)

        dict_result = dic_vagas[index_vaga]

    return {'success': dict_result}


def formatar_output(output_content):
    
    prompt = f"""
    Por favor, organize e formate a [DESCRIÇÃO DA VAGA] a seguir em uma estrutura clara e legível. 
    Não crie nenhum texto, somente utilize o conteúdo da [DESCRIÇÃO DA VAGA]. 
    Corrija erros de pontuação e utilize Markdown para a formatação, garantindo que o texto seja fácil de ler e bem estruturado.
    
    UTILIZE A SEGUINTE ESTRUTURA:
    Sobre a Empresa: Escreva uma breve introdução sobre a empresa, somente se houver na descrição.
    Responsabilidades e Atribuições: Liste as principais responsabilidades da posição em formato de lista.
    Requisitos e Qualificações: Liste os requisitos e qualificações necessárias, também em formato de lista.
    Diferenciais: Inclua uma seção para diferenciais que podem ser considerados um plus para a vaga.
    
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
    load_dotenv()
    key_gemini = os.getenv('GEMINI_KEY')

    genai.configure(api_key=key_gemini)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return {"success": response.text}