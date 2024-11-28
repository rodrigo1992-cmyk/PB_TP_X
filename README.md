# RESPOSTAS ao TP4
## Projeto Disponível em: https://github.com/rodrigo1992-cmyk/PB_TP_X/tree/PB_TP4
## Para visualizar no Streamlit, executar arquivo "app\pages\app_streamlit.py"
## Para subir o servidor com uvicorn, executar o arquivo "app\services\main_backend.py"

# 1. Identificação e Escolha do Modelo LLM (Local):
Critérios de Seleção: Pesquise e selecione o modelo de linguagem natural mais adequado para a sua aplicação, considerando os seguintes critérios:
Desempenho: Avalie a precisão, a capacidade de resposta e o tipo de tarefa para a qual o modelo foi treinado (ex: GPT, BERT, T5).
Custo Computacional Local: Verifique os recursos de hardware necessários para rodar o modelo no ambiente local (como GPU, memória RAM, etc.).
Acessibilidade Local: Garanta que o modelo escolhido pode ser carregado localmente, utilizando bibliotecas como Transformers da HuggingFace para download e execução do modelo em sua própria máquina.
Documentação: Justifique a escolha do modelo, detalhando os critérios de desempenho, custo computacional local e acessibilidade que levaram à sua decisão.
Integração de LLM com FastAPI no Ambiente Local:
Execução Local: Utilize um modelo da HuggingFace ou um modelo treinado localmente para realizar tarefas de processamento de linguagem natural (como geração de texto, resumo automático, classificação de sentimento, etc.) e integre-o ao seu backend FastAPI, sem necessidade de conexão com a nuvem.
Rota FastAPI: Implemente uma rota em FastAPI que se conecte ao modelo LLM rodando localmente para processar dados textuais fornecidos pela aplicação. Exemplo de rota:
POST /processar_texto: Rota que recebe um texto enviado pelo usuário e retorna a análise ou processamento realizado pelo modelo de linguagem, como um resumo ou análise de sentimento.
Execução Local do HuggingFace: Baixe o modelo diretamente em seu ambiente de desenvolvimento local e utilize as funções da biblioteca Transformers para carregar e executar o modelo sem depender de serviços externos.
Manipulação das Respostas da API:
Response Models: Crie Response Models em FastAPI para garantir que as respostas da API sejam consistentes e estruturadas, utilizando modelos de resposta claros e bem definidos.
Exemplo: A rota /processar_texto deve retornar um JSON estruturado com informações detalhadas, como o texto processado, o tipo de análise realizada (resumo, classificação, etc.) e os resultados gerados.
Validação das Respostas: Assegure-se de que todos os retornos da API estejam validados, garantindo que os dados enviados e recebidos estejam no formato correto e sejam compreensíveis para o cliente.
Tratamento Robusto de Erros na API:
Exceções HTTP: Implemente um tratamento robusto de erros na API, utilizando exceções HTTP específicas em FastAPI para lidar com problemas que possam ocorrer durante as requisições (como falha ao carregar o modelo, problemas com os dados de entrada, ou timeouts).
Exemplo: Se o modelo LLM não estiver carregado corretamente ou ocorrer um erro na manipulação dos dados, a aplicação deve retornar um código de erro adequado (ex: 503 Serviço Indisponível) e uma mensagem explicativa.
Melhoria da Experiência do Usuário: Garanta que os erros sejam tratados de forma clara e informativa, proporcionando feedback útil para o usuário final e facilitando o diagnóstico de possíveis problemas.
































--------------------------------------------------- REPOSTAS QUE TINHAM SIDO DADAS AO TP3------------------------------------------------------------------------------------
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
  >> * Definição das APIs no front-end: app/pages/utils.py
  >> * Uso das APIs no front-end: app/pages/app_streamlit.py  e  app/pages/page_vagas.py
  
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