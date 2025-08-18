# API de Busca Semântica com LangChain

Esta é uma API Flask que utiliza LangChain, Chroma e OpenAI para realizar buscas semânticas em uma base de conhecimento.

## Funcionalidades

- **Busca Semântica**: Utiliza embeddings da OpenAI para encontrar informações relevantes
- **Base de Conhecimento**: Armazena documentos em um banco vetorial Chroma
- **Geração de Respostas**: Usa GPT da OpenAI para gerar respostas contextualizadas
- **API REST**: Interface simples via HTTP

## Endpoints

### POST /api/ask
Faz uma pergunta à base de conhecimento.

**Corpo da requisição:**
```json
{
  "pergunta": "Sua pergunta aqui"
}
```

**Resposta de sucesso:**
```json
{
  "resposta": "Resposta gerada pela IA",
  "status": "success"
}
```

**Resposta de erro:**
```json
{
  "erro": "Descrição do erro",
  "status": "error"
}
```

### GET /api/health
Verifica se a API está funcionando.

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API está funcionando corretamente"
}
```

## Configuração Local

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd api-railway
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave da OpenAI:
```
OPENAI_API_KEY=sua_chave_openai_aqui
SECRET_KEY=sua_chave_secreta_aqui
```

5. **Execute a aplicação**
```bash
python src/main.py
```

A API estará disponível em `http://localhost:5000`

## Deploy no Railway

### Pré-requisitos
- Conta no [Railway](https://railway.app)
- Chave da API da OpenAI
- Base de conhecimento Chroma (pasta `db/`)

### Passos para Deploy

1. **Conecte seu repositório ao Railway**
   - Faça login no Railway
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório

2. **Configure as variáveis de ambiente**
   No painel do Railway, vá em "Variables" e adicione:
   ```
   OPENAI_API_KEY=sua_chave_openai_aqui
   SECRET_KEY=uma_chave_secreta_segura
   FLASK_ENV=production
   ```

3. **Upload da base de conhecimento**
   - Certifique-se de que a pasta `src/db/` com seus dados do Chroma está no repositório
   - Ou configure um volume persistente no Railway para armazenar os dados

4. **Deploy automático**
   - O Railway detectará automaticamente o `requirements.txt` e `Procfile`
   - O deploy será feito automaticamente

### Estrutura de Arquivos Importante

```
api-railway/
├── src/
│   ├── main.py          # Aplicação principal
│   ├── db/              # Base de dados Chroma (você precisa adicionar)
│   └── static/          # Arquivos estáticos (opcional)
├── requirements.txt     # Dependências Python
├── Procfile            # Comando de inicialização
├── railway.json        # Configurações do Railway
├── .env.example        # Exemplo de variáveis de ambiente
└── README.md           # Esta documentação
```

## Notas Importantes

1. **Base de Conhecimento**: Você precisa criar e popular a base de dados Chroma antes do deploy
2. **Variáveis de Ambiente**: Nunca commite arquivos `.env` com chaves reais
3. **Limites**: Configure limites apropriados para evitar custos excessivos da OpenAI
4. **Monitoramento**: Use os logs do Railway para monitorar a aplicação

## Exemplo de Uso

```bash
# Teste local
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Como funciona a busca semântica?"}'

# Teste em produção (substitua pela URL do Railway)
curl -X POST https://sua-app.railway.app/api/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "Como funciona a busca semântica?"}'
```

## Troubleshooting

- **Erro 500**: Verifique se a chave da OpenAI está configurada corretamente
- **Base vazia**: Certifique-se de que a pasta `db/` contém dados do Chroma
- **Timeout**: Ajuste os timeouts no Railway se necessário

