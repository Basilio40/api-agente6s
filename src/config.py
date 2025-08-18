import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações da aplicação"""
    
    # Configurações básicas do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV', 'production') == 'development'
    
    # Configurações da OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Configurações do Chroma
    CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "db")
    
    # Configurações da busca semântica
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.7'))
    MAX_RESULTS = int(os.getenv('MAX_RESULTS', '4'))
    
    # Configurações de rate limiting (se necessário no futuro)
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '60'))
    
    @staticmethod
    def validate_config():
        """Valida se as configurações obrigatórias estão presentes"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY é obrigatória")
        
        return True

