# RESPOSTAS ao TP5
## Projeto Disponível em: https://github.com/rodrigo1992-cmyk/PB_TP_X/tree/PB_TP5
## Para visualizar no Streamlit, executar arquivo "app\pages\app_streamlit.py"
## Para subir o servidor com uvicorn, executar o arquivo "app\services\main_backend.py"

# 1. Atualização e Completação dos Artefatos do TSDP (Team Data Science Process):
* Revise e complete todos os artefatos do TDSP, que orientaram seu processo de ciência de dados ao longo do projeto.
* Data Summary Report: Detalhe como os dados coletados via APIs ou web scraping foram integrados e utilizados ao longo do projeto.
* Project Charter: Atualize e argumente sobre como os dados, o uso de IA e a engenharia de prompts estão alinhados com a resolução do problema de negócio escolhido, destacando sua relevância no contexto de Ciência de Dados.
* Certifique-se de que a documentação reflita o ciclo completo de ciência de dados, desde a obtenção dos dados até a transformação deles em insights por meio de IA.

> Arquivos disponíveis dentro da pasta "docs", a saber: "Bussiness Model Canvas.png", "Project Charter.pptx", "Wireframe Lo-Fi.png", "Solution Architecture Diagram.png", "Model Report.md" e "Data Summary Report.txt".

# 2. Escolha de um Caminho para a Solução Final com LLMs (Local ou via API): 
O aluno deve optar por um dos três caminhos abaixo, integrando-o de maneira eficaz ao ciclo de ciência de dados do projeto. A solução deve fazer uso dos dados coletados, aplicando as técnicas de IA e engenharia de prompts no processamento e análise dessas informações.

* **Opção 1**: Implementação de Memória Conversacional com LLMs
Integre LLMs para implementar memória conversacional na sua aplicação, permitindo que o sistema mantenha o contexto ao longo de várias interações.
<br>
**Ciência de Dados Aplicada**: A memória conversacional pode ser aplicada para interpretar perguntas e manter o histórico de interações ao lidar com grandes volumes de dados sobre sustentabilidade ou governança, fornecendo insights contínuos e contextualizados a partir dos dados analisados.
<br>
Exemplo: O sistema pode relembrar informações anteriores e adaptar suas respostas com base nos dados coletados sobre ESG, com a memória sendo gerenciada por modelos locais ou APIs de IA online como o ChatGPT.

* **Opção 2**: Automação de Sumarização de Textos com LLMs
Utilize LLMs para automatizar a sumarização de grandes volumes de dados textuais (como relatórios ou artigos sobre ESG).
<br>
**Ciência de Dados Aplicada**: Aqui, o foco é em sintetizar informações complexas e densas, transformando dados coletados em resumos claros e acionáveis, facilitando a tomada de decisões baseada em dados.
<br>
Exemplo: Ao usar dados textuais obtidos via web scraping ou APIs, como relatórios de sustentabilidade, o sistema pode gerar resumos automáticos, tornando o processamento e a análise de grandes documentos mais eficiente. A sumarização pode ser realizada com modelos locais ou APIs de IA online como OpenAI.

* **Opção 3**: Desenvolvimento de Agentes Inteligentes para Tomada de Decisão
Implemente agentes inteligentes capazes de resolver problemas complexos com base nos dados coletados.
<br>
**Ciência de Dados Aplicada**: Esses agentes podem automatizar a análise dos dados coletados sobre indicadores de desempenho ESG, sugerindo recomendações ou previsões baseadas em padrões encontrados nos dados.
Exemplo: Um agente pode ser configurado para analisar dados financeiros e de sustentabilidade, propondo ações corretivas ou recomendações baseadas em benchmarks de governança, utilizando modelos locais ou APIs de IA online.

> O Sistema utiliza Modelos de LLM para duas aplicações diferentes:
> * Modelo Local para Extração de entidades nomeadas (NER) das descrições de vagas, para criação de uma base de dados de requisitos, que é utilizada em filtros e gráficos.
> * Chat para busca de vagas por similaridade com a descrição inputada pelo usuário via chat no streamlit, feito em 3 etapas:
>   - **1° Etapa** - O input do usuário é passado para o GEMINI para que ele avalie se é um input para busca ou uma frase indiferente, como um "Bom dia", neste caso ele interage com o usuário pedindo que seja informada a descrição de uma vaga. Utilizada engenharia de prompt para orientar a avaliar o input para instruir quanto ao retorno no caso de um input válido ou inválido.
>   - **2° Etapa** - Se o input for válido é executado um modelo local que usa embedding para calcular a semelhança entre a setença inputada e as descrições das vagas na base de dados.
>   - **3° Etapa** - Os dados da vaga localizada são passados novamente para o Gemini, para que ele estruture o conteúdo de forma padronizada e formate como markdown, para melhorar a visualização ao exibir no chat. Utilizada engenharia de prompt para orientar o modelo a como separar o conteúdo em sessões e para que ele siga o template de markdown fornecido.

# 3. Desenvolvimento de um Dashboard Final com Modelos de IA: 
Após implementar a funcionalidade escolhida (memória conversacional, sumarização ou agente inteligente), integre-a a um dashboard interativo que demonstre claramente o ciclo de Ciência de Dados, desde a coleta dos dados até a geração de insights. O dashboard deve:
<br>
* Exibir os dados coletados e processados ao longo do projeto, mostrando como os modelos de IA foram aplicados para transformar esses dados em conhecimento útil.
> Disponível nas sessões "JobFinder" e "Data Download" no aplicativo.

* Oferecer visualizações e gráficos que ilustrem os principais resultados, insights ou recomendações gerados pelos modelos de IA.
> Disponível na sessão "Profile Analysis" no aplicativo.

* Permitir que o usuário interaja com os dados e modelos de IA, seja utilizando modelos locais ou APIs de IA online, para obter respostas em tempo real baseadas no contexto de sustentabilidade e governança.
> Disponível na sessão "JobFinder" no aplicativo.

# 4. Apresentação e Argumentação da Solução Final:
* Além da implementação técnica, você deverá apresentar a solução e justificar como ela resolve o problema de negócio, destacando a importância de cada etapa do ciclo de ciência de dados (da coleta e limpeza à modelagem e apresentação).
* Destaque o uso de dados reais e como os modelos de IA aplicados oferecem insights relevantes para a governança e sustentabilidade, alinhando a solução aos ODS e práticas de ESG.
* A simplicidade no uso do dashboard, combinada com a profundidade dos insights gerados, será um critério importante na avaliação.

> Material da apresentação disponível na sessão "About" do aplicativo
