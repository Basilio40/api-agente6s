import logging
from typing import List, Tuple, Optional
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SemanticSearchService:
    """Serviço para busca semântica usando LangChain e Chroma"""
    
    def __init__(self):
        self.config = Config()
        self.embedding_function = None
        self.db = None
        self.llm = None
        self.prompt_template = """
Responda a pergunta do usuário:
{pergunta} 

com base nessas informações abaixo:

{base_conhecimento}"""
        
    def initialize(self):
        """Inicializa os componentes necessários"""
        try:
            logger.info("Inicializando serviço de busca semântica...")
            
            # Inicializar função de embedding com a chave da API
            self.embedding_function = OpenAIEmbeddings(openai_api_key=self.config.OPENAI_API_KEY)
            
            # Inicializar banco de dados Chroma
            self.db = Chroma(
                persist_directory=self.config.CHROMA_DB_PATH,
                embedding_function=self.embedding_function
            )
            
            # Inicializar modelo de linguagem com a chave da API
            self.llm = ChatOpenAI(openai_api_key=self.config.OPENAI_API_KEY, temperature=0)
            
            logger.info("Serviço de busca semântica inicializado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao inicializar serviço de busca semântica: {str(e)}")
            return False
    
    def search_knowledge_base(self, query: str) -> Tuple[List[str], float]:
        """
        Busca na base de conhecimento
        
        Args:
            query: Pergunta do usuário
            
        Returns:
            Tuple com lista de textos relevantes e score de relevância
        """
        try:
            if not self.db:
                raise ValueError("Base de dados não inicializada")
            
            # Realizar busca por similaridade
            results = self.db.similarity_search_with_relevance_scores(
                query, 
                k=self.config.MAX_RESULTS
            )
            
            if not results:
                logger.warning(f"Nenhum resultado encontrado para: {query}")
                return [], 0.0
            
            # Verificar se os resultados são relevantes
            best_score = results[0][1] if results else 0.0
            
            if best_score < self.config.SIMILARITY_THRESHOLD:
                logger.info(f"Resultados abaixo do threshold ({best_score} < {self.config.SIMILARITY_THRESHOLD})")
                return [], best_score
            
            # Extrair textos dos resultados
            relevant_texts = [result[0].page_content for result in results]
            
            logger.info(f"Encontrados {len(relevant_texts)} resultados relevantes (score: {best_score})")
            return relevant_texts, best_score
            
        except Exception as e:
            logger.error(f"Erro na busca: {str(e)}")
            raise
    
    def generate_response(self, query: str, knowledge_base: List[str]) -> str:
        """
        Gera resposta usando o modelo de linguagem
        
        Args:
            query: Pergunta do usuário
            knowledge_base: Lista de textos relevantes da base de conhecimento
            
        Returns:
            Resposta gerada pelo modelo
        """
        try:
            if not self.llm:
                raise ValueError("Modelo de linguagem não inicializado")
            
            # Combinar textos da base de conhecimento
            combined_knowledge = "\n\n----\n\n".join(knowledge_base)
            
            # Criar prompt
            prompt = ChatPromptTemplate.from_template(self.prompt_template)
            formatted_prompt = prompt.invoke({
                "pergunta": query,
                "base_conhecimento": combined_knowledge
            })
            
            # Gerar resposta
            response = self.llm.invoke(formatted_prompt)
            
            logger.info("Resposta gerada com sucesso")
            return response.content
            
        except Exception as e:
            logger.error(f"Erro na geração de resposta: {str(e)}")
            raise
    
    def process_query(self, query: str) -> dict:
        """
        Processa uma pergunta completa
        
        Args:
            query: Pergunta do usuário
            
        Returns:
            Dicionário com resposta e metadados
        """
        try:
            # Validar entrada
            if not query or not query.strip():
                return {
                    "erro": "Pergunta vazia ou inválida",
                    "status": "error"
                }
            
            # Buscar na base de conhecimento
            relevant_texts, score = self.search_knowledge_base(query.strip())
            
            if not relevant_texts:
                return {
                    "resposta": "Não encontrei informações relevantes na base de conhecimento.",
                    "status": "success",
                    "metadata": {
                        "relevance_score": score,
                        "sources_found": 0
                    }
                }
            
            # Gerar resposta
            response = self.generate_response(query.strip(), relevant_texts)
            
            return {
                "resposta": response,
                "status": "success",
                "metadata": {
                    "relevance_score": score,
                    "sources_found": len(relevant_texts)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro no processamento da pergunta: {str(e)}")
            return {
                "erro": str(e),
                "status": "error"
            }

# Instância global do serviço
semantic_service = SemanticSearchService()

