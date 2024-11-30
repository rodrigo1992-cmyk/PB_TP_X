import csv
import os
import pandas as pd

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



with open(dic_paths['csv_vagas_norm'], mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]  
    
    df = pd.DataFrame(data)
    print(df.dtypes)


