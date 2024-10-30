import sys
sys.path.append(r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP_X')

from functions_webscrapping import *
from functions_dataPreProcessing import *
from app.router.paths import * #Apontar para o meu arquivo de rotas, que irá conter as funções de API
from fastapi import FastAPI
import uvicorn

dic_paths = dicionario_paths()

def webscrapping_catho():
    lista_cargos = ['cientista-de-dados', 'analista-de-dados', 'engenheiro-de-dados', 'analista-bi']
    
    #Realiza o request nas páginas de busca para cada cargo na lista_cargos, até o máximo de 11 páginas por cargo
    soup_paginas_de_busca = obter_paginas_de_busca(lista_cargos, 11)
    print(soup_paginas_de_busca)

    #Raspa as páginas de busca e salva os links de cada vaga em um arquivo csv
    links = raspas_paginas_e_salvar_links(soup_paginas_de_busca, dic_paths['csv_links'])
    print(links)

    #Itera sobre os links salvos e salva cada página de vaga em um arquivo html separado
    iterar_links_e_salvar_paginas_html(dic_paths['csv_links'], dic_paths['folder_htmls'])

    #Itera sobre os arquivos html salvos e extrai os dados de cada vaga
    df_final = iterar_htmls_e_extrair_dados(dic_paths['csv_links'], dic_paths['folder_htmls'], dic_paths['csv_vagas'])

    #Confere a quantidade de parses com sucesso
    print(df_final.shape)

def webscrapping_indeed():
    lista_cargos = ['cientista+de+dados', 'analista+de+dados', 'engenheiro+de+dados', 'analista+bi']
    
    #Os intervalos são de 10 em 10, então de 0 a 21 serãoexecutadas 3 iterações (0, 10 e 20)
    #raspas_paginas_e_salvar_links_indeed(lista_cargos, dic_paths['csv_links_indeed'], start_range=30, end_range=51)
    iterar_paginas_e_extrair_dados_indeed(dic_paths['csv_links_indeed'], dic_paths['csv_vagas_indeed'], start_iter= 0, end_iter=361)

def dataPreProcessing():

    Juntar_datasets_vagas(dic_paths['csv_vagas_catho'], dic_paths['csv_vagas_indeed'], dic_paths['csv_vagas'])
    Pre_Processamento_Df_Vagas(dic_paths['csv_vagas'], dic_paths['csv_vagas_norm'])
    Pre_Processamento_Df_Requisitos(dic_paths['csv_lista_ferramentas'], dic_paths['csv_vagas_norm'], dic_paths['csv_requisitos'])


#-----------------------EXECUÇÃO-----------------------
app = FastAPI()
app.include_router(router)

#Estão comentadas as funções de webscrapping e dataPreProcessing para não serem executadas toda vez que o código for rodado
if __name__ == "__main__":
    #webscrapping_catho()
    #webscrapping_indeed()
    dataPreProcessing()
    #uvicorn.run(app, host="0.0.0.0", port=8000)