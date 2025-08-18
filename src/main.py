import os
import sys
import logging
from datetime import datetime

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from src.config import Config
from src.semantic_search import semantic_service

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Factory function para criar a aplicação Flask"""
    
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    
    # Configurações
    try:
        Config.validate_config()
        app.config.from_object(Config)
        logger.info("Configurações carregadas com sucesso")
    except Exception as e:
        logger.error(f"Erro nas configurações: {str(e)}")
        raise
    
    # CORS
    CORS(app, origins="*")
    
    # Inicializar serviço de busca semântica
    if not semantic_service.initialize():
        logger.error("Falha ao inicializar serviço de busca semântica")
        # Em produção, você pode querer falhar aqui ou usar um fallback
    
    @app.before_request
    def log_request_info():
        """Log das requisições recebidas"""
        if request.endpoint != 'health_check':  # Evitar spam de health checks
            logger.info(f"Requisição: {request.method} {request.path} - IP: {request.remote_addr}")
    
    @app.after_request
    def after_request(response):
        """Log das respostas enviadas"""
        if request.endpoint != 'health_check':
            logger.info(f"Resposta: {response.status_code} para {request.method} {request.path}")
        return response
    
    @app.errorhandler(404)
    def not_found(error):
        """Handler para erro 404"""
        return jsonify({
            "erro": "Endpoint não encontrado",
            "status": "error",
            "code": 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handler para erro 500"""
        logger.error(f"Erro interno: {str(error)}")
        return jsonify({
            "erro": "Erro interno do servidor",
            "status": "error",
            "code": 500
        }), 500
    
    @app.route('/api/ask', methods=['POST'])
    def perguntar():
        """Endpoint principal para fazer perguntas à base de conhecimento"""
        try:
            # Validar Content-Type
            if not request.is_json:
                return jsonify({
                    "erro": "Content-Type deve ser application/json",
                    "status": "error"
                }), 400
            
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "erro": "Dados JSON inválidos ou vazios",
                    "status": "error"
                }), 400

            pergunta = data.get('pergunta')
            if not pergunta or not isinstance(pergunta, str) or not pergunta.strip():
                return jsonify({
                    "erro": "Campo 'pergunta' é obrigatório e deve ser uma string não vazia",
                    "status": "error"
                }), 400

            # Processar pergunta
            logger.info(f"Processando pergunta: {pergunta[:100]}...")
            resultado = semantic_service.process_query(pergunta)
            
            # Adicionar timestamp
            resultado['timestamp'] = datetime.utcnow().isoformat()
            
            status_code = 200 if resultado.get('status') == 'success' else 500
            return jsonify(resultado), status_code

        except Exception as e:
            logger.error(f"Erro não tratado em /api/ask: {str(e)}")
            return jsonify({
                "erro": "Erro interno do servidor",
                "status": "error",
                "timestamp": datetime.utcnow().isoformat()
            }), 500

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Endpoint para verificar se a API está funcionando"""
        try:
            # Verificar se o serviço de busca está funcionando
            service_status = "healthy" if semantic_service.db is not None else "degraded"
            
            return jsonify({
                "status": "healthy",
                "service_status": service_status,
                "message": "API está funcionando corretamente",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            })
        except Exception as e:
            logger.error(f"Erro no health check: {str(e)}")
            return jsonify({
                "status": "unhealthy",
                "message": "Erro no health check",
                "timestamp": datetime.utcnow().isoformat()
            }), 500

    @app.route('/api/info', methods=['GET'])
    def api_info():
        """Informações sobre a API"""
        return jsonify({
            "name": "API de Busca Semântica",
            "version": "1.0.0",
            "description": "API para busca semântica usando LangChain e OpenAI",
            "endpoints": {
                "POST /api/ask": "Fazer uma pergunta à base de conhecimento",
                "GET /api/health": "Verificar status da API",
                "GET /api/info": "Informações sobre a API"
            },
            "timestamp": datetime.utcnow().isoformat()
        })

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        """Servir arquivos estáticos ou informações da API"""
        static_folder_path = app.static_folder
        
        if static_folder_path and path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'index.html') if static_folder_path else None
            if index_path and os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'index.html')
            else:
                # Retornar informações da API como fallback
                return jsonify({
                    "message": "API de Busca Semântica",
                    "version": "1.0.0",
                    "endpoints": {
                        "POST /api/ask": "Fazer uma pergunta à base de conhecimento",
                        "GET /api/health": "Verificar status da API",
                        "GET /api/info": "Informações sobre a API"
                    },
                    "documentation": "Consulte o README.md para mais informações",
                    "timestamp": datetime.utcnow().isoformat()
                })

    return app

# Criar aplicação
app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    logger.info(f"Iniciando aplicação na porta {port} (debug={debug})")
    app.run(host='0.0.0.0', port=port, debug=debug)

