## Funcionalidades e Navegação
O dashboard foi projetado para ser intuitivo, permitindo que o gestor de frota navegue entre diferentes níveis de detalhamento através da Barra Lateral (Sidebar).

Barra Lateral de Controle
Seletor de Visão: Alterna instantaneamente todo o dashboard entre:

Visão Geral: Métricas macro de toda a operação.

Visão Motoristas: Foco em performance individual e comportamento.

Visão Veículos: Status de utilização e ociosidade por placa.

Filtros Dinâmicos: Permite filtrar os dados por data, turno ou motorista específico, atualizando todos os KPIs e gráficos simultaneamente.

Painel de Indicadores (KPIs)
Cartões de Resumo: Visualização rápida do total de registros, porcentagem de ociosidade e total de horas dentro/fora da cerca (Geofencing).

Status em Tempo Real: Indicadores de cores que destacam pontos de atenção na frota.

Análise Geoespacial e Temporal
Mapa de Concentração: Exibição do polígono da cerca com a plotagem dos pontos de ociosidade, facilitando a identificação visual de onde os veículos param.

Gráficos de Tendência: Histogramas e gráficos de linha que mostram a Evolução Diária e os Picos por Hora, ajudando a identificar gargalos em horários específicos do dia.

Exportação de Dados
Download de Relatórios: Na parte inferior de cada visão, o usuário tem acesso a um botão para exportar a base de dados filtrada e tratada para o formato .csv, pronta para uso em outras ferramentas.


## Como Usar
Siga os passos abaixo para replicar o ambiente e rodar o dashboard localmente:

1. Clonar o Repositório
Abra o terminal e baixe o projeto:
->  git clone https://github.com/joaogabriel7/Analisys.git
->  cd Analisys


2. Configurar o Ambiente Virtual (Recomendado)
Para manter as dependências organizadas e evitar conflitos com outros projetos de Python:
-> python3 -m venv venv
-> source venv/bin/activate


3. Instalar Dependências
Instale as bibliotecas necessárias (Pandas, Streamlit, Shapely, etc.):
-> pip install -r requirements.txt


4. Preparar as Bases de Dados
Certifique-se de que as 6 bases de dados estão localizadas na pasta correta para que o código encontre os caminhos relativos:
-> Localização esperada: src/data/

6. Executar o Dashboard
Agora, basta iniciar o servidor do Streamlit:
-> streamlit run src/dashboard.py

Após o comando, o dashboard abrirá automaticamente no seu navegador no endereço http://localhost:8501.

## Deploy (Streamlit Cloud)
O projeto também está configurado para deploy contínuo. Link do App: *https://dashboard-interativo-4lwtqmtjptpjg2dvrdezmy.streamlit.app/.*
