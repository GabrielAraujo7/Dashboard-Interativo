# Dashboard de Ociosidade

Este projeto apresenta um dashboard Streamlit com 3 visões:
- Visão Motoristas (apenas registros dentro da cerca)
- Visão Veículos (apenas registros dentro da cerca)
- Visão Geral (todos os registros, com destaque dentro/fora da cerca)

O dashboard também gera base consolidada de dados e permite download CSV.

---

## Pré-requisitos

- Python 3.11+ (o ambiente aqui usa 3.13)
- `pip` instalado

## Instalação

```bash
cd /home/joaogabriel7/Downloads/Analisys
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Estrutura de arquivos

- `src/dashboard.py` : aplicação Streamlit
- `requirements.txt` : dependências
- `data/` : arquivos Excel (coordenadas + relatórios semanais)

## Execução local

```bash
source env/bin/activate
streamlit run src/dashboard.py
```

## Observações de path

O `dashboard.py` original usa caminhos absolutos, por isso no deploy é recomendado atualizar para caminhos relativos ou provisionar os arquivos em `data/`.

Exemplo:
```python
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
DF_PATH = BASE_DIR / 'data' / 'relatorio_semanal_V-1001.xlsx'
```

## Deploy rápido (Streamlit Cloud)

1. Faça push do código para GitHub.
2. Acesse https://streamlit.io/cloud e conecte GitHub.
3. Crie novo app apontando para `src/dashboard.py`.
4. Streamlit fará o deploy automático.

## Build alternativo (Heroku / VPS / Docker)

### Docker (recomendado se não usar Streamlit Cloud)

Crie `Dockerfile` (padrão):
```Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "src/dashboard.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

```bash
docker build -t dashboard-ociosidade .
docker run -d -p 8501:8501 dashboard-ociosidade
```

## Validar antes da entrega

- `streamlit run src/dashboard.py` localmente
- checar sidebar e 3 visões
- checar mapa com polígono de cerca
- baixar CSV de consolidados
- conferir arquivo gerado: `data/consolidado.csv`
