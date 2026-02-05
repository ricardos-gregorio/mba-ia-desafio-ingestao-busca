PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

load_dotenv()


DB_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "gpt5_collection")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
GOOGLE_EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL", "gpt-5-nano")
GOOGLE_LLM_MODEL = os.getenv("GOOGLE_LLM_MODEL", "gemini-2.5-flash-lite")

def search_prompt(question=None):
  if not question:
    question = input("PERGUNTA: ")
  if not DB_URL:
    print("DATABASE_URL não configurada.")
    return None

  # Carregar embeddings e vetorstore
  if EMBEDDING_PROVIDER == "gemini":
    embeddings = GoogleGenerativeAIEmbeddings(
      model=GOOGLE_EMBEDDING_MODEL,
      google_api_key=GOOGLE_API_KEY
    )
  else:
    embeddings = OpenAIEmbeddings(
      model=OPENAI_EMBEDDING_MODEL,
      openai_api_key=OPENAI_API_KEY
    )

  vectorstore = PGVector.from_existing_index(
    embedding=embeddings,
    collection_name=COLLECTION_NAME,
    connection=DB_URL
  )

  # Buscar contexto relevante
  results = vectorstore.similarity_search_with_score(question, k=10)
  contexto = "\n".join([doc.page_content for doc, _ in results])

  prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

  # Chamar LLM
  if LLM_PROVIDER == "gemini":
    llm = ChatGoogleGenerativeAI(
      model=GOOGLE_LLM_MODEL,
      google_api_key=GOOGLE_API_KEY
    )
  else:
    llm = ChatOpenAI(
      model=OPENAI_LLM_MODEL,
      openai_api_key=OPENAI_API_KEY
    )
  response = llm.invoke(prompt)
  return response.content