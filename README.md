-------------RESUMO DAS ENTREGAS--------

# RESPOSTAS ao TP2
#### Configuração do Ambiente de Desenvolvimento:
  * Configure seu ambiente de desenvolvimento, incluindo Git para controle de versão e preparação para deploy. Lembre-se de seguir a estrutura do CRISP-DM para organizar seu projeto de forma eficiente e escalável.
  
  >> Substituí a utilização do CondaEnv pelo PipEnv, "docs\bussiness docs\PipEnv.png"

#### Implementação de Interface de Usuário Dinâmica:
  * Evolua a interface inicial da sua aplicação Streamlit, acrescentando elementos de interatividade que permitam ações dinâmicas por parte do usuário. A interface deve ser intuitiva e funcional, garantindo uma boa experiência de uso.
  

#### Extração de Conteúdo da Web para alimentar a aplicação:
  * Utilize a ferramenta Beautiful Soup para extrair conteúdo de páginas web. Execute esses códigos separadamente e armazene os dados obtidos em arquivos CSV e/ou TXT nos diretórios de data/.
  
  >> O Projeto inicialmente previa a raspagem do Linkedin, porém a página estava me bloqueando ao tentar realizar as iterações. Também tentei no Indeed e no Vagas.com, sem sucesso. Creio que com o Sellenium conseguiria, porém como o requisito era fazer com BeautifulSoup só consegui no site da Catho, e obtive bons resultados, raspando 420 páginas.

  >> O Site da Catho possui menos vagas anunciadas, tendo poucas para cientista de dados. Em vista disso expandi o propósito do projeto para profissionais de dados em geral, raspando vagas de Cientistas de Dados, Engenheiros de Dados e Analistas de Dados.

  >> No notebook "webscrapping.ipynb" primeiro foi feito foi criado e testado o código célula por célula, somente depois encapsulei em funções, criando o arquivo functions_webscrapping.py.

  >> Por último mudei a forma de obter os dados, invés de buscar as tags individuais, que não tinham classes ou ids claros, busquei a div "props" e depois tratei como um Json para resgatar cada campo dentro da div.

  * Posteriormente, utilize esses dados para alimentar a interface da aplicação: exiba informações relevantes geradas a partir do conteúdo obtido, como nuvens de palavras e estatísticas básicas (tabelas, notícias).
  
#### Cache e Estado de Sessão:
  * Implemente cache e estado de sessão em Streamlit para melhorar a performance da aplicação e garantir a persistência dos dados em aplicações interativas. Isso permitirá que os dados sejam mantidos ao longo das interações do usuário, proporcionando uma experiência mais fluida
  
#### Serviço de Upload e Download de Arquivos:
  * Desenvolva um serviço de upload e download de arquivos em Streamlit, permitindo que o usuário adicione mais informações ao sistema através de arquivos CSV. Esses dados devem complementar as informações já exibidas na aplicação, tornando-a mais robusta e informativa.
  
#### Finalização do Project Charter e Data Summary Report:
  * Complete o Project Charter e o Data Summary Report, detalhando o escopo, os objetivos, os stakeholders do projeto, e as fontes de dados utilizadas. 
  >> Os documentosn estão em "docs\bussiness docs\Project Charter.png" e "docs\data docs\Data Summary Report.txt"
