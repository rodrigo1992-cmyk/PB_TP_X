from app.services.functions_webscrapping import *

def main():
    lista_cargos = ['cientista-de-dados', 'analista-de-dados', 'engenheiro-de-dados', 'analista-bi']
    links_path = r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP1\app\data\raw\links_vagas.csv'
    htmls_folder_path = r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP1\app\data\html_pages'
    path_csv_resultado = r'C:\Users\RodrigoPintoMesquita\Documents\GitHub\PB_TP1\app\data\processed\vagas.csv'

    soup_paginas_de_busca = obter_paginas_de_busca(lista_cargos, 11)
    print(soup_paginas_de_busca)
    
    links = raspas_paginas_e_salvar_links(soup_paginas_de_busca, links_path)
    print(links)

    iterar_links_e_salvar_paginas_html(links_path, htmls_folder_path)

    df_final = iterar_htmls_e_extrair_dados(links_path, htmls_folder_path, path_csv_resultado)

    #Conferir a quantidade de parses com sucesso
    print(df_final.shape)

if __name__ == "__main__":
    main()