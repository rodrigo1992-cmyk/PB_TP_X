# RESPOSTAS ao TP3
## Projeto Disponível em: https://github.com/rodrigo1992-cmyk/PB_TP_X/tree/PB_TP3
## Para visualizar no Streamlit, executar arquivo "app\streamlit\app_streamlit.py"
## Para subir o servidor com uvicorn, executar o arquivo "app\services\main_backend.py"

#### Revisão e Atualização da Documentação:
  * Revise o Project Charter e o Data Summary Report, atualizando a documentação para refletir as novas funcionalidades e decisões tomadas nesta fase do projeto.
  * Reavalie o problema de negócio à luz das novas ferramentas (como FastAPI e Selenium) e ajuste suas metas, se necessário.
  * Atualize a descrição das fontes de dados utilizadas, considerando possíveis novas fontes obtidas com scraping dinâmico.
  
  >> Não houve necessidade de revisão.

#### Criação de uma Aplicação com Múltiplas Páginas:
  * Evolua a interface da sua aplicação em Streamlit, implementando múltiplas páginas e um menu de navegação que permita ao usuário transitar facilmente entre diferentes seções da aplicação.
  * Cada página deve representar uma funcionalidade ou análise diferente, como a visualização de dados, gráficos interativos, upload/download de arquivos ou estatísticas geradas a partir dos dados coletados.
    
  >> Critérios já atendidos na entrega do TP2.

#### Extração de Dados de Páginas Dinâmicas (Web Scraping):
  * Utilize o Selenium para realizar o web scraping de páginas dinâmicas, se necessário. Caso seu projeto utilize uma fonte de dados que exija interação com elementos dinâmicos (como formulários ou carregamentos assíncronos), o Selenium será essencial. Observação: Se não houver necessidade de utilizar Selenium, concentre-se no aprimoramento dos dados coletados com Beautiful Soup ou APIs, mantendo a simplicidade quando possível.
  * Armazene os dados obtidos em arquivos CSV ou TXT, organizando-os no diretório de data/ para uso na aplicação.
  
  >> Critérios já atendidos na entrega do TP2. Não foi necessário o uso do Selenium, pois consegui com o BS.
  
#### Desenvolvimento de APIs com FastAPI:
  * Configure o ambiente de desenvolvimento para a criação de APIs com FastAPI.
  * Crie uma API simples com rotas e endpoints que permitam interagir com os dados da aplicação. Exemplo de funcionalidades da API:
    * Consulta de dados (GET)
    * Envio de novos dados (POST)
  * Implemente ao menos duas rotas em sua API, e documente-as adequadamente, explicando sua função e como elas podem ser usadas para interação com os dados.
  
  >> Implementado o GET para obter os 2 datasets principais, e o POST para que o usuário possa carregar novas vagas. Verificar arquivos a seguir:
  >> * Iniciar o servidor: app/services/main_backend.py
  >> * Definição das APIs no back-end: app/router/paths.py
  >> * Definição das APIs no front-end: app/streamlit/utils.py
  >> * Uso das APIs no front-end: app/streamlit/app_streamlit.py  e  app/streamlit/page_vagas.py
  
#### Preparação para Uso de Inteligência Artificial com LLMs:
  * Nesta etapa, comece a pensar nos dados que você coletou até agora e como eles podem ser utilizados em tarefas baseadas em LLMs nas próximas entregas.
  * Considere os tipos de dados disponíveis e as possíveis aplicações com LLMs, como:
    * Análise de Texto Gerado: Usar os dados coletados para gerar resumos automáticos de textos longos, facilitando a compreensão e análise de documentos.
    * Classificação de Sentimentos: Aplicar um modelo de LLM para classificar os sentimentos em textos (positivos, negativos ou neutros) coletados de notícias, redes sociais, ou outras fontes.
    * Perguntas e Respostas (Q&A): Usar um LLM para construir um sistema de perguntas e respostas a partir dos dados disponíveis, respondendo a perguntas relevantes com base nos conteúdos coletados.
Geração de Texto: Automatizar a criação de relatórios ou insights com base nos dados brutos, utilizando LLMs para gerar textos descritivos.
  * Mantenha o foco na preparação do projeto para que, na próxima etapa, as funcionalidades de IA via LLM sejam facilmente integradas e aplicadas a esses cenários.

>> Inicialmente, criei de forma manual a lista de hard-skills a serem buscados nas descrições das vagas (arquivo "ferramentas.csv"). Na próxima etapa utilizarei o LLM para criar a lista de forma automática a partir da análise das descrições das vagas. Creio que o resultado será melhor pois irá encontrar ferramentas não listadas originalmente e variações de escrita.
>> Utilizarei o LLM para criar diferentes categorias de vagas de acordo com a análise das funções contidas nas descrições.
>> Utilizarei o LLM para que o usuário possa fazer uma adequação automática do seu currículo, para maior adesão às vagas que ele selecionar.