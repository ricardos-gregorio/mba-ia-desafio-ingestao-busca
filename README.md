# Desafio MBA Engenharia de Software com IA - Full Cycle
Ingestão e Busca Semântica com LangChain e Postgres
Ingestão: Ler um arquivo PDF e salvar suas informações em um banco de dados PostgreSQL com extensão pgVector.
Busca: Permitir que o usuário faça perguntas via linha de comando (CLI) e receba respostas baseadas apenas no conteúdo do PDF.

## Como executar a solução

1. **Pré-requisitos:**
	- Docker e Docker Compose instalados
	- Python 3.12 instalado
	- (Opcional) Ambiente virtual Python configurado

2. **Suba o banco de dados Postgres com extensão pgvector:**
	```bash
	docker-compose up -d
	```

3. **Instale as dependências Python:**
	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```

4. **Configure o arquivo `.env`:**
	- Certifique-se de que as variáveis `DATABASE_URL`, `PG_VECTOR_COLLECTION_NAME` e `PDF_PATH` estejam corretas.
	- Exemplo:
	  ```env
	  DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/rag
	  PG_VECTOR_COLLECTION_NAME=gpt5_collection
	  PDF_PATH=document.pdf
	  ```

5. **Coloque o arquivo PDF desejado na raiz do projeto** (exemplo: `document.pdf`).

6. **Ingestão do PDF para o banco vetorial:**
	```bash
	python src/ingest.py
	```

7. **Executar o chat para perguntas e respostas:**
	```bash
	python src/chat.py
	```

---

## Como o sistema funciona

O sistema realiza a ingestão de um arquivo PDF, dividindo-o em pequenos trechos (chunks) e gerando embeddings desses textos usando modelos da OpenAI ou Google Gemini. Esses embeddings são armazenados em um banco de dados PostgreSQL com a extensão pgvector, permitindo buscas semânticas.

Quando o usuário faz uma pergunta pelo `chat.py`, o sistema busca os trechos mais relevantes no banco vetorial, monta um contexto e envia para o modelo responder de forma contextualizada.

**Principais componentes:**
- `src/ingest.py`: Faz a ingestão do PDF para o banco vetorial.
- `src/search.py`: Realiza buscas semânticas no banco vetorial.
- `src/chat.py`: Interface de perguntas e respostas usando o contexto recuperado.

**Fluxo resumido:**
1. PDF → Splitter → Embeddings → Banco Vetorial
2. Pergunta → Busca Semântica → Contexto → Resposta