.PHONY: help start stop restart logs migrate makemigrations shell test format lint superuser collectstatic clean

# Variáveis
COMPOSE = docker compose
WEB_SERVICE = challenge_web
DB_SERVICE = challenge_db
N8N_SERVICE = challenge_n8n

# Comandos principais
help: ## Mostra esta ajuda
	@echo "🚀 Sistema de Leads - Comandos disponíveis:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

start: ## Inicia o projeto
	@echo "📦 Iniciando o projeto..."
	$(COMPOSE) up -d --build
	@echo "✅ Projeto iniciado!"
	@echo "🌐 Django: http://localhost:8000"
	@echo "🔧 N8N: http://localhost:5678"

stop: ## Para o projeto
	@echo "🛑 Parando o projeto..."
	$(COMPOSE) down
	@echo "✅ Projeto parado!"

restart: ## Reinicia o projeto
	@echo "🔄 Reiniciando o projeto..."
	$(COMPOSE) down
	$(COMPOSE) up -d --build
	@echo "✅ Projeto reiniciado!"

logs: ## Mostra logs em tempo real
	@echo "📝 Mostrando logs..."
	$(COMPOSE) logs -f

logs-web: ## Mostra logs do Django
	$(COMPOSE) logs -f $(WEB_SERVICE)

logs-db: ## Mostra logs do PostgreSQL
	$(COMPOSE) logs -f $(DB_SERVICE)

logs-n8n: ## Mostra logs do N8N
	$(COMPOSE) logs -f $(N8N_SERVICE)

migrate: ## Executa migrações
	@echo "🗄️ Executando migrações..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py migrate
	@echo "✅ Migrações executadas!"

makemigrations: ## Cria migrações
	@echo "📝 Criando migrações..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py makemigrations
	@echo "✅ Migrações criadas!"

shell: ## Abre shell do Django
	@echo "🐍 Abrindo shell do Django..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py shell

test: ## Executa testes
	@echo "🧪 Executando testes..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py test

test-verbose: ## Executa testes com output detalhado
	@echo "🧪 Executando testes com output detalhado..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py test -v 2

format: ## Formata código (black + isort)
	@echo "🎨 Formatando código..."
	$(COMPOSE) exec $(WEB_SERVICE) black .
	$(COMPOSE) exec $(WEB_SERVICE) isort .
	@echo "✅ Código formatado!"

lint: ## Verifica código (flake8)
	@echo "🔍 Verificando código..."
	$(COMPOSE) exec $(WEB_SERVICE) flake8 .
	@echo "✅ Verificação concluída!"

superuser: ## Cria superusuário
	@echo "👤 Criando superusuário..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py createsuperuser

collectstatic: ## Coleta arquivos estáticos
	@echo "📦 Coletando arquivos estáticos..."
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py collectstatic --noinput
	@echo "✅ Arquivos estáticos coletados!"

clean: ## Limpa containers e volumes
	@echo "🧹 Limpando containers e volumes..."
	$(COMPOSE) down -v
	docker system prune -f
	@echo "✅ Limpeza concluída!"

status: ## Mostra status dos containers
	@echo "📊 Status dos containers:"
	$(COMPOSE) ps

backup: ## Faz backup do banco de dados
	@echo "💾 Fazendo backup do banco..."
	$(COMPOSE) exec $(DB_SERVICE) pg_dump -U leads_user leads_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Backup criado!"

restore: ## Restaura backup do banco (use: make restore FILE=backup.sql)
	@echo "🔄 Restaurando backup..."
	@if [ -z "$(FILE)" ]; then echo "❌ Especifique o arquivo: make restore FILE=backup.sql"; exit 1; fi
	$(COMPOSE) exec -T $(DB_SERVICE) psql -U leads_user leads_db < $(FILE)
	@echo "✅ Backup restaurado!"

# Comandos de desenvolvimento
dev: start migrate ## Inicia o projeto em modo desenvolvimento
	@echo "🚀 Projeto iniciado em modo desenvolvimento!"
	@echo "📝 Para ver logs: make logs"
	@echo "🧪 Para executar testes: make test"

setup: ## Configuração inicial do projeto
	@echo "⚙️ Configurando projeto..."
	@if [ ! -f .env ]; then cp env.example .env; echo "✅ Arquivo .env criado"; fi
	$(COMPOSE) up -d --build
	$(COMPOSE) exec $(WEB_SERVICE) python manage.py migrate
	@echo "✅ Configuração concluída!"
	@echo "🌐 Acesse: http://localhost:8000"

# Comandos de produção
prod-build: ## Build para produção
	@echo "🏗️ Fazendo build para produção..."
	$(COMPOSE) -f docker-compose.yml build --no-cache
	@echo "✅ Build concluído!"

prod-start: ## Inicia em modo produção
	@echo "🚀 Iniciando em modo produção..."
	$(COMPOSE) up -d
	@echo "✅ Produção iniciada!"

# Comandos de debug
debug: ## Inicia em modo debug
	@echo "🐛 Iniciando em modo debug..."
	$(COMPOSE) up
	@echo "✅ Debug iniciado!"

shell-db: ## Abre shell do PostgreSQL
	@echo "🗄️ Abrindo shell do PostgreSQL..."
	$(COMPOSE) exec $(DB_SERVICE) psql -U leads_user leads_db

# Comandos de monitoramento
monitor: ## Monitora recursos dos containers
	@echo "📊 Monitorando recursos..."
	docker stats

health: ## Verifica saúde dos serviços
	@echo "🏥 Verificando saúde dos serviços..."
	@echo "Django:"
	@curl -f http://localhost:8000/health/ || echo "❌ Django não está respondendo"
	@echo "N8N:"
	@curl -f http://localhost:5678/healthz || echo "❌ N8N não está respondendo"
	@echo "PostgreSQL:"
	@$(COMPOSE) exec $(DB_SERVICE) pg_isready -U leads_user || echo "❌ PostgreSQL não está respondendo"

