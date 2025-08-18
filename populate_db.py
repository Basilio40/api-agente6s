import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from src.config import Config

# Carregar variáveis de ambiente
load_dotenv()

PASTA_BASE = "base"

def criar_db():
    """Função principal para criar o banco de dados Chroma a partir de PDFs."""
    print("🚀 Iniciando criação da base de dados a partir de PDFs...")
    
    # Validar configurações
    try:
        Config.validate_config()
    except ValueError as e:
        print(f"❌ Erro de configuração: {str(e)}")
        return False

    # Verificar se a pasta base existe e contém PDFs
    if not os.path.exists(PASTA_BASE) or not any(Path(PASTA_BASE).glob("*.pdf")):
        print(f"⚠️ Aviso: A pasta \'{PASTA_BASE}\' não existe ou não contém arquivos PDF.")
        print("   Por favor, crie a pasta e adicione seus arquivos PDF nela.")
        print("   Criando documentos de exemplo para demonstração...")
        documents = create_sample_documents()
    else:
        print(f"📂 Carregando documentos da pasta \'{PASTA_BASE}\'...")
        documents = carregar_documentos()
        if not documents:
            print(f"❌ Erro: Nenhum documento PDF válido encontrado na pasta \'{PASTA_BASE}\'")
            return False

    print(f"📄 Documentos carregados: {len(documents)}")
    chunks = dividir_chunks(documents)
    print(f"✂️ Documentos divididos em {len(chunks)} chunks.")
    
    try:
        vetorizar_chunks(chunks)
        print("🎉 Base de Dados criada com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao vetorizar chunks: {str(e)}")
        return False

def carregar_documentos():
    """Carrega documentos PDF da pasta base."""
    carregador = PyPDFDirectoryLoader(PASTA_BASE, glob="*.pdf")
    documentos = carregador.load()
    return documentos

def dividir_chunks(documentos):
    """Divide os documentos em chunks menores."""
    separador_documentos = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )
    chunks = separador_documentos.split_documents(documentos)
    return chunks

def vetorizar_chunks(chunks):
    """Vetoriza os chunks e os armazena no banco de dados Chroma."""
    db_path = Config.CHROMA_DB_PATH
    os.makedirs(db_path, exist_ok=True)
    
    # Passar a chave da OpenAI explicitamente
    embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
    
    db = Chroma.from_documents(chunks, embeddings, persist_directory=db_path)
    print(f"💾 Banco de Dados Chroma criado em: {os.path.abspath(db_path)}")

def create_sample_documents():
    """Cria documentos de exemplo para demonstração se não houver PDFs na pasta base."""
    sample_docs = [
        {
            "content": """
            A busca semântica é uma técnica de recuperação de informação que vai além da correspondência exata de palavras-chave. 
            Ela utiliza o significado e contexto das palavras para encontrar informações relevantes, mesmo quando as palavras 
            exatas não estão presentes no documento. Isso é possível através do uso de embeddings, que são representações 
            vetoriais de texto que capturam o significado semântico.
            """,
            "metadata": {"source": "conceitos_ia", "topic": "busca_semantica"}
        },
        {
            "content": """
            O LangChain é um framework para desenvolvimento de aplicações com modelos de linguagem. Ele fornece ferramentas 
            para conectar LLMs a fontes de dados externas, criar chains de processamento complexas, e gerenciar memória 
            e contexto em conversas. O LangChain suporta diversos provedores de LLM como OpenAI, Anthropic, e modelos 
            open-source através do Hugging Face.
            """,
            "metadata": {"source": "frameworks", "topic": "langchain"}
        },
        {
            "content": """
            O Chroma é um banco de dados vetorial open-source projetado para aplicações de IA. Ele permite armazenar 
            embeddings de documentos e realizar buscas por similaridade de forma eficiente. O Chroma suporta diferentes 
            funções de distância, metadados, e pode ser usado tanto em memória quanto com persistência em disco.
            """,
            "metadata": {"source": "bancos_dados", "topic": "chroma"}
        },
        {
            "content": """
            A OpenAI oferece diversos modelos de linguagem através de sua API, incluindo GPT-3.5, GPT-4, e modelos 
            especializados para embeddings como text-embedding-ada-002. Estes modelos podem ser usados para geração 
            de texto, análise, tradução, e criação de embeddings para busca semântica.
            """,
            "metadata": {"source": "apis", "topic": "openai"}
        },
        {
            "content": """
            Flask é um micro-framework web para Python que é leve e flexível. Ele é ideal para criar APIs REST, 
            aplicações web pequenas a médias, e protótipos. Flask fornece o essencial para desenvolvimento web 
            e permite adicionar extensões conforme necessário, como Flask-CORS para CORS e Flask-SQLAlchemy para ORM.
            """,
            "metadata": {"source": "frameworks", "topic": "flask"}
        }
    ]
    
    documents = []
    for doc_data in sample_docs:
        doc = Document(
            page_content=doc_data["content"].strip(),
            metadata=doc_data["metadata"]
        )
        documents.append(doc)
    
    return documents

if __name__ == "__main__":
    print("=" * 50)
    print("  POPULAÇÃO DA BASE DE DADOS CHROMA")
    print("  (A partir de PDFs na pasta 'base/' ou dados de exemplo)")
    print("=" * 50)
    
    success = criar_db()
    
    if success:
        print("\n✅ Processo concluído com sucesso!")
        print("   Agora você pode executar a API com: python src/main.py")
    else:
        print("\n❌ Processo falhou. Verifique os erros acima.")
        sys.exit(1)


