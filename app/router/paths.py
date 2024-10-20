import os

def dic_paths():
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