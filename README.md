# Sistema de Leads

Sistema simples para gerenciar leads com Django, PostgreSQL e N8N.

## Como Usar

### 1. Iniciar
```bash
docker compose up -d
```

### 2. Acessar
- **Django**: http://localhost:8000
- **N8N**: http://localhost:5678 (admin/admin123)

### 3. Configurar N8N
1. Acesse http://localhost:5678
2. Importe o workflow: `n8n-workflows/lead-webhook.json`
3. Ative o workflow (toggle verde)

## Funcionalidades

- ✅ Cadastrar leads
- ✅ Listar leads com busca
- ✅ Editar leads
- ✅ Excluir leads
- ✅ Dashboard com estatísticas
- ✅ Webhook automático para N8N
- ✅ Admin Django

## Estrutura

```
├── leads/                 # App Django
├── templates/            # Templates HTML
├── static/              # CSS/JS/Imagens
├── n8n-workflows/       # Workflows N8N
├── docker-compose.yml   # Containers
└── requirements.txt     # Dependências Python
```

## Comandos Úteis

```bash
# Testes
docker compose exec challenge_web python manage.py test

# Admin
docker compose exec challenge_web python manage.py createsuperuser

# Logs
docker compose logs -f
```

## Variáveis de Ambiente

Copie `env.example` para `.env` e configure:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=leads_db
DB_USER=leads_user
DB_PASSWORD=leads_password
N8N_WEBHOOK_URL=http://challenge_n8n:5678/webhook/lead-received
N8N_USER=admin
N8N_PASSWORD=admin123
```

