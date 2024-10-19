
import streamlit as st
import pandas as pd

st.title("Radar de Vagas DS")
st.write("**Escopo**: Ao consolidar e analisar as competências requisitadas por cada empresa, o projeto apoia a inserção de profissionais no mercado de trabalho, contribuindo para a geração de empregos e o desenvolvimento de uma força de trabalho com qualificação alinhada ao mercado. Isso não só ajuda os profissionais a encontrar melhores oportunidades de trabalho, mas também fortalece a economia ao atender à demanda das empresas por talentos qualificados. Este visa atender à ODS 8 (Trabalho Decente e Crescimento Econômico).")
st.write("""
**Objetivos**: Desenvolver uma aplicação web que consolide anúncios de vagas de cientista de dados no LinkedIn, analisando as competências e funções mais solicitadas por nível de vaga.
* Coletar dados de anúncios de vagas de cientista de dados no LinkedIn.
* Utilizar modelo LLM para analisar descrições de vagas e identificar competências e funções especificadas.
* Desenvolver visualizações em Streamlit para apresentar os resultados.
* Oferecer insights para candidatos, recrutadores e instituições de ensino sobre tendências de mercado.
""")

st.write("Acesse este link para visualizar a página de onde serão coletados os dados, já com exemplo de filtro. (https://www.linkedin.com/jobs/search?keywords=Cientista%20De%20Dados&location=Rio%20de%20Janeiro%2C%20Rio%20de%20Janeiro%2C%20Brasil&geoId=106701406&distance=0&f_TPR=&position=1&pageNum=0)")
st.write("Link para uma inspiração visual (https://www.behance.net/gallery/198960873/Job-finder-dashboard?tracking_source=search_projects|job+dashboard&l=2)")
st.write("Abaixo, segue um exemplo/amostra dos dados que serão coletados:")

df = pd.read_csv('app\data\processed\Exemplo_Amostra_Dados.csv')
st.dataframe(df)
