

import pandas as pd
import requests
from bs4 import BeautifulSoup
import random
import time
import os
import re
import json

def obter_paginas_de_busca(lista_cargos, range_max):
    """
    Através do Request, esta função obtém os resultados de pesquisa no site da Catho 
    para cada cargo passado na lista fornecida, e retorna um objeto BeautifulSoup
    contendo o conteúdo HTML de todas as páginas obtidas.

    Args:
        lista_cargos (list): Uma lista de strings representando os cargos a serem buscados.
        range_max (int): O número máximo de páginas a serem buscadas para cada cargo.

    Returns:
        BeautifulSoup: Um objeto BeautifulSoup contendo o HTML de todas as páginas obtidas.
    """

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"}
    lista_soups = []

    for cargo in lista_cargos:
       for page in range(1, range_max):
          intervalo = random.uniform(2, 5)
          time.sleep(intervalo)

          url = f'https://www.catho.com.br/vagas/{cargo}/?page={page}'

          response = requests.get(url, headers=headers)
          if response.status_code == 200:
             soup = BeautifulSoup(response.text, 'html.parser')
             lista_soups.append(soup)
          else:
             print(f'Erro no cargo {cargo}, página {page}: {response.status_code}')

    soup_paginas_de_busca = BeautifulSoup('', 'html.parser')
    for s in lista_soups:
       soup_paginas_de_busca.append(s)
    return soup_paginas_de_busca

def raspas_paginas_e_salvar_links(soup_paginas_de_busca, links_path):
    """
    Esta função procura por links de vagas no objeto BeautifulSoup fornecido,
    extrai esses links e os salva em um arquivo CSV no caminho especificado.

    Args:
        soup_paginas_de_busca (BeautifulSoup): Objeto BeautifulSoup contendo o HTML das páginas de busca.
        links_path (str): Caminho do arquivo CSV onde os links serão salvos.

    Returns:
        list: Uma lista contendo todos os links extraídos.
    """
    conteudo = soup_paginas_de_busca.find_all('h2', {'class': 'Title-module__title___3S2cv'})
    links = []
    for c in conteudo:
        try:
            link = c.find('a').get('href')
            links.append(link)
        except: 
            pass

    df = pd.DataFrame(list(set(links)))
    df.to_csv(links_path, index=False, header=False)
    
    return links


def iterar_links_e_salvar_paginas_html(links_path, htmls_folder_path):
    """
    Esta função lê links de um arquivo CSV, faz requisições HTTP para cada link
    e salva o conteúdo HTML de cada página em arquivos separados no caminho fornecido.

    Args:
        links_path (str): Caminho do arquivo CSV contendo os links das vagas.
        htmls_folder_path (str): Caminho da pasta onde os arquivos HTML serão salvos.
    """

    with open(links_path, 'r') as file:
        links = file.read().splitlines()

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"}

    for i, url in enumerate(links, start=0):
        html_file = f'{htmls_folder_path}/page_{i}.html'

        intervalo = random.uniform(2, 5)
        time.sleep(intervalo)

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            html_content = response.text
            with open(html_file, 'w', encoding='utf-8') as file:
                file.write(html_content)
        else:
            print(f'Erro na iteração: {i} | Status: {response.status_code} | Motivo: {response.reason}')


def iterar_htmls_e_extrair_dados_deprecada(links_path, htmls_folder_path, path_csv_resultado):
    """
    Esta foi a primeira função desenvolvida para extrair dados dos arquivos HTML obtidos das vagas pesquisadas, 
    usando apenas seletores CSS. Porém consegui uma forma melhor pegando do elemento "Props" da página e depois fazendo
    a leitura como um Json.
    """

    files = os.walk(htmls_folder_path)
    files = list(files)[0][2]
    paths_files = [f'{htmls_folder_path}/{file}' for file in files]

    df = pd.DataFrame(columns=['url','titulo', 'local', 'salario', 'regime', 'descricao'])
    df_urls = pd.read_csv(links_path, header=None)
    lista_urls = df_urls[0].tolist()

    for row_file in paths_files:
        with open(row_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
            indice = int(re.search(r'page_(\d+)\.html', row_file).group(1))
            url = lista_urls[indice]
            
        soup_vaga = BeautifulSoup(html_content, 'html.parser')

        titulo_vaga = soup_vaga.find('h1')
        titulo_vaga = titulo_vaga.text if titulo_vaga else "não disponível"

        local_vaga = soup_vaga.find('div', {'class': 'cidades'})
        local_vaga = local_vaga.get_text() if local_vaga else "não disponível"

        salario_img = soup_vaga.find('img', {'alt': 'Um icone representando dinheiro'})
        salario_vaga = salario_img.find_parent('li').get_text() if salario_img else "não disponível"

        h3_reg = soup_vaga.find('h3', string="Regime de Contratação")
        regime = h3_reg.find_next('p').get_text() if h3_reg else "não disponível"

        descricao_vaga = soup_vaga.find('div', {'class': 'job-description'})
        descricao_vaga = descricao_vaga.get_text() if descricao_vaga else "não disponível"

        nova_linha = pd.DataFrame([{
            'url': url,
            'titulo': titulo_vaga,
            'local': local_vaga, 
            'salario': salario_vaga,
            'regime': regime, 
            'descricao': descricao_vaga
        }])

        df = pd.concat([df, nova_linha], ignore_index=True)

        df.to_csv(path_csv_resultado, index=False, quoting=1)

    return df


def iterar_htmls_e_extrair_dados(links_path, htmls_folder_path, path_csv_resultado):
    """
        --------------------------------NOVA FUNÇÃO------------------------
        Esta função lê todos os arquivos HTML obtidos das vagas pesquisadas, extrai informações como título,
        local, salário, regime e descrição, e salva em um arquivo csv

        Args:
            links_path (str): Caminho do arquivo CSV contendo os links das vagas.
            htmls_folder_path (str): Caminho da pasta contendo os arquivos HTML das vagas.

        Returns:
            pandas.DataFrame: Um DataFrame contendo as informações extraídas das vagas.

        Note:
            O DataFrame retornado contém as colunas: 'url', 'titulo', 'local', 'salario',
            'regime' e 'descricao'.
    """

    files = os.walk(htmls_folder_path)
    files = list(files)[0][2]
    paths_files = [f'{htmls_folder_path}/{file}' for file in files]

    df = pd.DataFrame(columns=['id_vaga', 'data_anuncio', 'titulo_vaga', 'titulo_resumo', 'faixa_salarial', 'empresa_contratante', 'estado', 'cidade', 'url', 'descricao', 'beneficios', 'regimeContrato'])

    for row_file in paths_files:
        with open(row_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

            try:
                soup = BeautifulSoup(html_content, 'html.parser')

                script = soup.find('script', id='__NEXT_DATA__')

                json_data = json.loads(script.string)
                json_data_job = json_data['props']['pageProps']['jobAdData']

                id_vaga = json_data_job.get('id', "não disponível")
                data_anuncio = json_data_job.get('data', "não disponível")
                titulo_vaga = json_data_job.get('titulo', "não disponível")
                titulo_resumo = json_data.get('query', {}).get('slug', "não disponível")[0]
                faixa_salarial = json_data_job.get('faixaSalarial', "não disponível")
                empresa_contratante = json_data_job.get('contratante', {}).get('nome', "não disponível")
                estado = json_data_job.get('vagas', [{}])[0].get('uf', "não disponível")
                cidade = json_data_job.get('vagas', [{}])[0].get('cidade', "não disponível")
                url = json_data['props']['pageProps']['pathname']
                descricao = json_data_job.get('descricao', "não disponível")
                descricao = descricao.replace('\n', '')
                beneficios = json_data_job.get('benef', "não disponível")
                regime_contrato = json_data_job.get('regimeContrato', "não disponível")


                nova_linha = pd.DataFrame([{
                    "id_vaga": id_vaga,
                    "data_anuncio": data_anuncio,
                    "titulo_vaga": titulo_vaga,
                    "titulo_resumo": titulo_resumo,
                    "faixa_salarial": faixa_salarial,
                    "empresa_contratante": empresa_contratante,
                    "estado": estado,
                    "cidade": cidade,
                    "url": url,
                    "descricao": descricao,
                    "beneficios": beneficios,
                    "regimeContrato": regime_contrato
                }])

                df = pd.concat([df, nova_linha], ignore_index=True)

            except:
                print(f'Erro na iteração: {row_file}')
            
        df.to_csv(path_csv_resultado, index=False, quoting=1, encoding='utf-8')

    return df
