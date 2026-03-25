Como Usar
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

Deploy (Streamlit Cloud)
O projeto também está configurado para deploy contínuo. Ao realizar um push para a branch main, o Streamlit Cloud atualiza automaticamente a versão online.
Link do App: https://dashboard-interativo-4lwtqmtjptpjg2dvrdezmy.streamlit.app/.
