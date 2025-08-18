import os
import sys
from datetime import datetime

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/ask', methods=['POST'])
def perguntar():
    """Endpoint simplificado para teste"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"erro": "Dados JSON inválidos ou vazios"}), 400

        pergunta = data.get('pergunta')
        if not pergunta or not isinstance(pergunta, str) or not pergunta.strip():
            return jsonify({"erro": "Campo 'pergunta' é obrigatório"}), 400

        # Resposta simulada para teste
        return jsonify({
            "resposta": f"Você perguntou: '{pergunta}'. Esta é uma resposta de teste da API Flask. A integração com LangChain será configurada após o deploy.",
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "mode": "test"
        })

    except Exception as e:
        return jsonify({
            "erro": str(e),
            "status": "error",
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        "status": "healthy",
        "message": "API está funcionando corretamente",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0-test"
    })

@app.route('/')
def home():
    """Página inicial da API"""
    return jsonify({
        "message": "API de Busca Semântica - Modo de Teste",
        "version": "1.0.0-test",
        "endpoints": {
            "POST /api/ask": "Fazer uma pergunta (modo teste)",
            "GET /api/health": "Verificar status da API"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

