Dashboard de Análise de Ociosidade (Streamlit)
Este projeto é uma solução de inteligência logística desenvolvida para monitorar a eficiência de frotas. Ele transforma dados brutos de telemetria e coordenadas em indicadores visuais para facilitar a tomada de decisão sobre ociosidade e geofencing.

Como Visualizar e Usar o Dashboard
Para explorar as análises, utilize o menu lateral (sidebar) para navegar entre as três visões principais:

1. Visão Motoristas (Foco em Operação)
O que você vê: Uma lista filtrada apenas com os registros que ocorreram dentro da cerca virtual.

Como usar: Ideal para identificar quais motoristas estão passando mais tempo em zonas de carga/descarga ou áreas de espera específicas.

2. Visão Veículos (Foco em Ativos)
O que você vê: Performance individualizada por unidade (placa/veículo), considerando apenas dados dentro da geocerca.

Como usar: Utilize os filtros para analisar o comportamento de um veículo específico e comparar sua ociosidade em relação à média da frota.

3. Visão Geral (Panorama Completo)
O que você vê: Um mapa interativo e gráficos que mostram todos os registros capturados.

Destaque Visual: Os pontos são diferenciados por cores para separar o que está "Dentro" vs. "Fora" da cerca.

Como usar: Tenha uma visão macro do deslocamento da frota e identifique gargalos logísticos fora das áreas previstas.

Exportação de Dados
O dashboard não é apenas visual. Na barra lateral ou ao final das tabelas, você encontrará a opção de Download CSV:

O sistema consolida automaticamente as 6 bases de dados em um único arquivo limpo.

Útil para auditorias externas ou integrações com outras ferramentas de BI (como Qlik Sense ou Power BI).

Como rodar o projeto
Se você deseja executar este dashboard localmente:

Prepare o ambiente:

Bash
python -m venv env
source env/bin/activate  # No Windows: .\env\Scripts\activate
pip install -r requirements.txt
Inicie a aplicação:

Bash
streamlit run src/dashboard.py
Acesse no navegador:
O Streamlit abrirá automaticamente o endereço http://localhost:8501.

Estrutura Técnica
data/: Repositório das bases Excel (Fontes de dados).

src/dashboard.py: O "cérebro" da aplicação e interface.

requirements.txt: Bibliotecas necessárias (Pandas, Streamlit, etc).

Desenvolvido por João Gabriel Estudante de Ciência da Computação & Analista de BI
