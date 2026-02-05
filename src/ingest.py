
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH", "document.pdf")
DB_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME", "gpt5_collection")

def ingest_pdf():
    if not PDF_PATH or not os.path.exists(PDF_PATH):
        print(f"Arquivo PDF não encontrado: {PDF_PATH}")
        return
    if not DB_URL:
        print("DATABASE_URL não configurada.")
        return

    print(f"Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    print(f"Dividindo PDF em chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = splitter.split_documents(documents)


    print(f"Gerando embeddings...")
    embedding_provider = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
    if embedding_provider == "gemini":
        embeddings = GoogleGenerativeAIEmbeddings(
            model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"),
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        embeddings = OpenAIEmbeddings(
            model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    print(f"Conectando ao banco e salvando vetores...")
    vectorstore = PGVector.from_documents(
        docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection=DB_URL,
    )
    print(f"Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()