import streamlit as st
import pandas as pd
from utils import *

def exibir():

    st.title("Radar de Vagas DS")
    st.write("""
             ## ESCOPO
             Ao consolidar e analisar as competências requisitadas por cada empresa, o projeto apoia a inserção de profissionais no mercado de trabalho, contribuindo para a geração de empregos e o desenvolvimento de uma força de trabalho com qualificação alinhada ao mercado. Isso não só ajuda os profissionais a encontrar melhores oportunidades de trabalho, mas também fortalece a economia ao atender à demanda das empresas por talentos qualificados. Este visa atender à ODS 8 (Trabalho Decente e Crescimento Econômico).

             ---
             ## OBJETIVOS 
             Disponibilizar vagas para profissionais de dados, analisando as competências e funções mais solicitadas por nível de vaga.
             * Coletar dados de anúncios de vagas de cientista de dados no LinkedIn.
             * Utilizar modelo LLM para analisar descrições de vagas e identificar competências e funções especificadas.
             * Desenvolver visualizações em Streamlit para apresentar os resultados.
             * Oferecer insights para candidatos, recrutadores e instituições de ensino sobre tendências de mercado.

             ---
             ## SESSÕES DO APP

             ### Job Finder
             Chat bot alimentado por IA que auxilia o usuário a encontrar vagas de emprego de acordo com a descrição desejada.

             ### Profile Analysis
             Sessão dedicada a compreensão e comparação dos diferentes profissionais de dados, analisando volumetria de vagas, distribuição geográfica, faixa salarial e competências mais solicitadas por perfil.
             
             ### Data Download
             Funções para download da base de dados de vagas, de acordo com os filtros selecionados pelo usuário, ou para cadastro de novas vagas através do download de base em csv.
             
             ---
             ## DOCUMENTAÇÃO
             * **Project Charter:** [Clique Aqui](https://github.com/rodrigo1992-cmyk/PB_TP_X/blob/PB_TP5/docs/bussiness%20docs/Project%20Charter.png)
             * **Bussiness Model Canvas:** [Clique Aqui](https://github.com/rodrigo1992-cmyk/PB_TP_X/blob/PB_TP5/docs/bussiness%20docs/Bussiness%20Model%20Canvas.png)
             * **Solution Architecture Diagram:** [Clique Aqui](https://github.com/rodrigo1992-cmyk/PB_TP_X/blob/PB_TP5/docs/data%20docs/Solution%20Architecture%20Diagram.pptx)
             * **Model Report:** [Clique Aqui](https://github.com/rodrigo1992-cmyk/PB_TP_X/blob/PB_TP5/docs/data%20docs/Model%20Report.md)
             * **Data Summary Report:** [Clique Aqui](https://github.com/rodrigo1992-cmyk/PB_TP_X/blob/PB_TP5/docs/data%20docs/Data%20Summary%20Report.txt)

            """)

