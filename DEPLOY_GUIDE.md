# Guia de Deploy no Railway - API de Busca Semântica

## 📋 Resumo do Projeto

Sua API Flask foi transformada em um projeto completo e otimizado para deploy no Railway. O projeto inclui:

- ✅ Estrutura organizada com separação de responsabilidades
- ✅ Tratamento robusto de erros e logging
- ✅ Configurações para produção
- ✅ Documentação completa
- ✅ Scripts de setup e população da base de dados

## 🚀 Deploy Rápido no Railway

### 1. Preparação
```bash
# 1. Faça upload do projeto para um repositório Git (GitHub, GitLab, etc.)
git init
git add .
git commit -m "Initial commit - API de Busca Semântica"
git remote add origin <seu-repositorio>
git push -u origin main
```

### 2. Deploy no Railway
1. Acesse [railway.app](https://railway.app)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Escolha seu repositório
5. Configure as variáveis de ambiente:
   ```
   OPENAI_API_KEY=sua_chave_openai_aqui
   SECRET_KEY=uma_chave_secreta_segura
   FLASK_ENV=production
   ```

### 3. Configuração da Base de Dados
Antes do primeiro uso, você precisa popular a base de dados:

```bash
# Execute localmente ou via Railway CLI
python populate_db.py
```

## 📁 Estrutura do Projeto

```
api-railway/
├── src/
│   ├── main.py              # Aplicação principal otimizada
│   ├── main_simple.py       # Versão de teste (opcional)
│   ├── config.py            # Configurações centralizadas
│   ├── semantic_search.py   # Lógica de busca semântica
│   └── static/              # Arquivos estáticos (se necessário)
├── requirements.txt         # Dependências simplificadas
├── requirements_final.txt   # Dependências com versões exatas
├── Procfile                # Comando de inicialização
├── railway.json            # Configurações do Railway
├── populate_db.py          # Script para popular base de dados
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos a ignorar no Git
├── README.md               # Documentação completa
└── DEPLOY_GUIDE.md         # Este guia
```

## 🔧 Melhorias Implementadas

### Código Original vs. Novo
- **Estrutura**: Código organizado em módulos separados
- **Configuração**: Sistema de configuração centralizado
- **Logging**: Sistema de logs detalhado para debugging
- **Tratamento de Erros**: Handlers específicos para diferentes tipos de erro
- **Validação**: Validação robusta de entrada de dados
- **Documentação**: Endpoints documentados e exemplos de uso

### Novos Endpoints
- `GET /api/health` - Status da API
- `GET /api/info` - Informações da API
- `GET /` - Página inicial com informações

## 🛠️ Comandos Úteis

### Desenvolvimento Local
```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Popular base de dados
python populate_db.py

# Executar API
python src/main.py
```

### Teste da API
```bash
# Health check
curl -X GET https://sua-app.railway.app/api/health

# Fazer pergunta
curl -X POST https://sua-app.railway.app/api/ask \
  -H "Content-Type: application/json" \
  -d '{"pergunta": "O que é busca semântica?"}'
```

## 🔒 Segurança e Produção

- ✅ CORS configurado adequadamente
- ✅ Variáveis de ambiente para dados sensíveis
- ✅ Logging para monitoramento
- ✅ Tratamento de erros sem exposição de dados internos
- ✅ Validação de entrada robusta

## 📊 Monitoramento

O Railway fornece logs automáticos. Para monitorar sua API:

1. Acesse o dashboard do Railway
2. Vá na seção "Logs"
3. Monitore requisições e erros
4. Use o endpoint `/api/health` para health checks

## 🆘 Troubleshooting

### Problemas Comuns

1. **Erro 500 na inicialização**
   - Verifique se `OPENAI_API_KEY` está configurada
   - Verifique logs do Railway

2. **Base de dados vazia**
   - Execute `python populate_db.py` localmente
   - Faça upload da pasta `src/db/` para o repositório

3. **Timeout nas requisições**
   - Ajuste configurações de timeout no Railway
   - Otimize consultas na base de dados

### Logs Importantes
```
INFO - Configurações carregadas com sucesso
INFO - Serviço de busca semântica inicializado com sucesso
INFO - Iniciando aplicação na porta 5000
```

## 📈 Próximos Passos

1. **Monitoramento**: Configure alertas no Railway
2. **Backup**: Configure backup da base de dados
3. **Escalabilidade**: Monitore uso e ajuste recursos
4. **Segurança**: Implemente rate limiting se necessário
5. **Documentação**: Crie documentação da API com Swagger

## 📞 Suporte

- Documentação do Railway: [docs.railway.app](https://docs.railway.app)
- Logs da aplicação: Dashboard do Railway
- Código fonte: Consulte os comentários no código

---

**Sua API está pronta para produção! 🎉**

