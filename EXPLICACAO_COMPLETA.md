# 📚 Explicação Completa do Sistema de Leads

## 🎯 **O que é este projeto?**

Este é um **sistema de gerenciamento de leads** (pessoas interessadas em um produto/serviço). Imagine que você tem uma empresa e quer capturar informações de clientes potenciais - este sistema faz isso!

## 🏗️ **Arquitetura Geral**

O sistema é dividido em **3 partes principais** que trabalham juntas:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   DJANGO        │    │   POSTGRESQL    │    │      N8N        │
│   (Front/Back)  │◄──►│   (Banco)       │    │   (Automação)   │
│   Porta 8000    │    │   Porta 5432    │    │   Porta 5678    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🐳 **Docker - O que é e por que usar?**

### **O que é Docker?**
Docker é como uma **"caixa mágica"** que contém tudo que uma aplicação precisa para funcionar. Imagine que você tem um computador dentro de outro computador!

### **Por que usar Docker?**
- ✅ **Funciona igual em qualquer lugar** (Windows, Mac, Linux)
- ✅ **Não precisa instalar nada** no seu computador
- ✅ **Isolamento** - cada serviço fica separado
- ✅ **Facilidade** - um comando levanta tudo

### **Como funciona no nosso projeto:**
```yaml
# docker-compose.yml
services:
  challenge_web:    # Django (nossa aplicação)
  challenge_db:     # PostgreSQL (banco de dados)
  challenge_n8n:    # N8N (automação)
```

## 🐍 **Django - O que é e como funciona?**

### **O que é Django?**
Django é um **framework Python** para criar sites/aplicações web. É como um "kit de ferramentas" que facilita a criação de sites.

### **Por que Django?**
- ✅ **Rápido de desenvolver**
- ✅ **Seguro por padrão**
- ✅ **Admin automático**
- ✅ **ORM** (não precisa escrever SQL)

### **Como funciona no nosso projeto:**

#### **1. Modelo (Model) - O que é?**
```python
# leads/models.py
class Lead(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    status = models.CharField(default='novo')
    criado_em = models.DateTimeField(auto_now_add=True)
```

**Explicação:** O modelo é como uma **"tabela"** no banco de dados. Define quais informações vamos guardar sobre cada lead.

#### **2. View (Visão) - O que é?**
```python
# leads/views.py
def cadastrar_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()  # Salva no banco
            # Envia webhook para N8N
```

**Explicação:** A view é como um **"controlador"** que recebe as requisições do usuário e decide o que fazer.

#### **3. Template - O que é?**
```html
<!-- templates/leads/cadastrar_lead.html -->
<form method="post">
    <input name="nome" placeholder="Nome">
    <input name="email" placeholder="Email">
    <button type="submit">Cadastrar</button>
</form>
```

**Explicação:** O template é a **"página HTML"** que o usuário vê. É a interface visual.

#### **4. URL - O que é?**
```python
# leads/urls.py
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastrar/', views.cadastrar_lead, name='cadastrar_lead'),
]
```

**Explicação:** As URLs são como **"endereços"** que direcionam o usuário para a página certa.

### **Fluxo completo Django:**
1. **Usuário acessa** http://localhost:8000/cadastrar/
2. **URL** direciona para a view `cadastrar_lead`
3. **View** renderiza o template com o formulário
4. **Usuário preenche** e clica em "Cadastrar"
5. **View** recebe os dados, valida e salva no banco
6. **View** envia webhook para N8N
7. **View** redireciona para dashboard

## 🗄️ **PostgreSQL - O que é e por que usar?**

### **O que é PostgreSQL?**
PostgreSQL é um **banco de dados relacional**. É como uma **"biblioteca organizada"** onde guardamos todas as informações.

### **Por que PostgreSQL?**
- ✅ **Confiável** - usado por grandes empresas
- ✅ **Relacional** - dados organizados em tabelas
- ✅ **ACID** - garante integridade dos dados
- ✅ **Gratuito** e open source

### **Como funciona no nosso projeto:**
```sql
-- Tabela leads (criada automaticamente pelo Django)
CREATE TABLE leads_lead (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200),
    email VARCHAR(254),
    status VARCHAR(20) DEFAULT 'novo',
    criado_em TIMESTAMP DEFAULT NOW()
);
```

**Explicação:** O Django cria automaticamente esta tabela baseada no nosso modelo `Lead`.

## 🔄 **N8N - O que é e como funciona?**

### **O que é N8N?**
N8N é uma **plataforma de automação**. É como um **"robô"** que executa tarefas automaticamente quando algo acontece.

### **Por que N8N?**
- ✅ **Automação visual** - arrasta e solta
- ✅ **Webhooks** - recebe dados de outras aplicações
- ✅ **Integração** - conecta com muitos serviços
- ✅ **Workflows** - sequência de ações

### **Como funciona no nosso projeto:**

#### **1. Webhook - O que é?**
```json
// n8n-workflows/lead-webhook.json
{
  "nodes": [
    {
      "type": "webhook",
      "path": "lead-received",
      "method": "POST"
    }
  ]
}
```

**Explicação:** Webhook é como um **"endereço"** que recebe dados de outras aplicações. Quando o Django salva um lead, ele "chama" este endereço.

#### **2. Validação - Como funciona?**
```json
{
  "type": "if",
  "conditions": [
    "{{ $json.nome }} is not empty",
    "{{ $json.email }} is not empty"
  ]
}
```

**Explicação:** O N8N verifica se os dados recebidos estão corretos (nome e email não vazios).

#### **3. Resposta - O que acontece?**
```json
{
  "type": "respondToWebhook",
  "responseBody": {
    "ok": true,
    "message": "Lead recebido com sucesso!"
  }
}
```

**Explicação:** O N8N responde para o Django dizendo se deu tudo certo ou não.

## 🔧 **Como tudo funciona junto?**

### **Fluxo completo do sistema:**

```
1. Usuário acessa o site
   ↓
2. Django mostra formulário
   ↓
3. Usuário preenche e envia
   ↓
4. Django valida os dados
   ↓
5. Django salva no PostgreSQL
   ↓
6. Django envia webhook para N8N
   ↓
7. N8N recebe e valida
   ↓
8. N8N responde para Django
   ↓
9. Django mostra mensagem de sucesso
```

## 📋 **Requisitos do Desafio - Como atendemos?**

### **1. Docker/Compose ✅**
```yaml
# docker-compose.yml
services:
  challenge_web:    # Django
  challenge_db:     # PostgreSQL  
  challenge_n8n:    # N8N
```
**Como atendemos:** Três serviços com prefixo `challenge_` que sobem com `docker compose up -d --build`.

### **2. Django (back + front) ✅**
```python
# Página / com formulário
path('', views.dashboard, name='dashboard')
path('cadastrar/', views.cadastrar_lead, name='cadastrar_lead')

# Validação server-side + CSRF
class LeadForm(forms.ModelForm):
    def clean_email(self):
        # Validação personalizada

# Modelo Lead
class Lead(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    criado_em = models.DateTimeField(auto_now_add=True)
```
**Como atendemos:** Formulário na página principal, validação no servidor, CSRF habilitado, modelo Lead salvo no PostgreSQL.

### **3. Integração N8N ✅**
```python
# Envio de webhook
webhook_data = {
    'nome': lead.nome,
    'email': lead.email,
}
response = requests.post(webhook_url, json=webhook_data)
```
**Como atendemos:** Django envia POST JSON para webhook do N8N após salvar o lead.

### **4. Config via .env ✅**
```env
# .env.example
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=leads_db
N8N_WEBHOOK_URL=http://challenge_n8n:5678/webhook/lead-received
```
**Como atendemos:** Todas as configurações via variáveis de ambiente, com arquivo `.env.example`.

## 🎯 **Diferenciais Implementados**

### **1. Página /leads/ com busca e paginação ✅**
```python
def lista_leads(request):
    query = request.GET.get('q')
    if query:
        leads_list = leads_list.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query)
        )
    paginator = Paginator(leads_list, 10)
```

### **2. Mensagens de sucesso/erro ✅**
```python
messages.success(request, 'Lead cadastrado com sucesso!')
messages.warning(request, 'Erro ao enviar webhook')
```

### **3. Admin Django habilitado ✅**
```python
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'status', 'criado_em']
```

### **4. WhiteNoise para estáticos ✅**
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### **5. Dockerfile multi-stage ✅**
```dockerfile
# Build stage
FROM python:3.11-slim as builder
# Production stage  
FROM python:3.11-slim
```

### **6. Healthchecks ✅**
```yaml
healthcheck:
  test: ["CMD", "pg_isready", "-U", "leads_user"]
  interval: 30s
  timeout: 10s
  retries: 3
```

### **7. Testes unitários ✅**
```python
class LeadModelTest(TestCase):
    def test_lead_creation(self):
        lead = Lead.objects.create(nome="João", email="joao@teste.com")
        self.assertEqual(lead.status, "novo")
```

### **8. Limitação de logs ✅**
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "50m"
```

## 🧪 **Testes - Como funcionam?**

### **O que são testes?**
Testes são **códigos que verificam se nossa aplicação funciona corretamente**. É como um "inspetor de qualidade".

### **Tipos de testes no projeto:**

#### **1. Testes de Modelo**
```python
def test_lead_creation(self):
    lead = Lead.objects.create(nome="João", email="joao@teste.com")
    self.assertEqual(lead.nome, "João")
    self.assertEqual(lead.status, "novo")
```
**O que testa:** Se conseguimos criar leads corretamente.

#### **2. Testes de Formulário**
```python
def test_valid_form(self):
    form_data = {
        'nome': 'Maria Santos',
        'email': 'maria@teste.com'
    }
    form = LeadForm(data=form_data)
    self.assertTrue(form.is_valid())
```
**O que testa:** Se a validação dos formulários funciona.

#### **3. Testes de Views**
```python
def test_cadastrar_lead_view_post_valid(self):
    form_data = {'nome': 'João', 'email': 'joao@teste.com'}
    response = self.client.post(reverse('leads:cadastrar_lead'), form_data)
    self.assertEqual(response.status_code, 302)  # Redirect
```
**O que testa:** Se as páginas funcionam corretamente.

## 🔒 **Segurança - O que implementamos?**

### **1. CSRF (Cross-Site Request Forgery)**
```html
<form method="post">
    {% csrf_token %}
    <!-- campos do formulário -->
</form>
```
**O que é:** Protege contra ataques que tentam enviar dados falsos.

### **2. Validação Server-Side**
```python
def clean_email(self):
    email = self.cleaned_data.get('email')
    if Lead.objects.filter(email=email).exists():
        raise forms.ValidationError('Email já cadastrado')
```
**O que é:** Valida os dados no servidor, não apenas no navegador.

### **3. Variáveis de Ambiente**
```python
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```
**O que é:** Configurações sensíveis não ficam no código.

## 🚀 **Como executar o projeto?**

### **1. Pré-requisitos**
- Docker instalado
- Docker Compose instalado

### **2. Passos**
```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd kogui

# 2. Configure as variáveis
cp env.example .env

# 3. Execute o projeto
docker compose up -d --build

# 4. Execute as migrações (primeira vez)
docker compose exec challenge_web python manage.py migrate

# 5. Crie um superusuário (opcional)
docker compose exec challenge_web python manage.py createsuperuser
```

### **3. Acessos**
- **Django**: http://localhost:8000
- **N8N**: http://localhost:5678 (admin/admin123)
- **Admin Django**: http://localhost:8000/admin

## 📊 **Estrutura de Arquivos**

```
kogui/
├── docker-compose.yml          # Configuração dos containers
├── Dockerfile                  # Imagem da aplicação Django
├── requirements.txt            # Dependências Python
├── env.example                 # Exemplo de variáveis
├── README.md                   # Como usar o projeto
├── manage.py                   # Script Django
├── leads_system/              # Projeto Django
│   ├── settings.py            # Configurações
│   ├── urls.py                # URLs principais
│   └── wsgi.py                # Configuração WSGI
├── leads/                     # App de leads
│   ├── models.py              # Modelo Lead
│   ├── views.py               # Views
│   ├── forms.py               # Formulários
│   ├── admin.py               # Admin
│   ├── urls.py                # URLs do app
│   └── tests.py               # Testes
├── templates/                 # Templates HTML
│   ├── base.html              # Template base
│   └── leads/                 # Templates específicos
├── static/                    # Arquivos estáticos
│   ├── css/style.css          # CSS
│   └── img/logo.svg           # Logo
└── n8n-workflows/             # Workflows N8N
    └── lead-webhook.json      # Workflow principal
```

## 🎯 **Conceitos Importantes para Entender**

### **1. MVT (Model-View-Template)**
- **Model**: Define os dados (tabelas do banco)
- **View**: Lógica de negócio (controla o que acontece)
- **Template**: Interface visual (HTML que o usuário vê)

### **2. ORM (Object-Relational Mapping)**
```python
# Em vez de escrever SQL:
# INSERT INTO leads (nome, email) VALUES ('João', 'joao@teste.com');

# Escrevemos Python:
Lead.objects.create(nome='João', email='joao@teste.com')
```

### **3. Webhook**
É como um **"telefone"** entre aplicações. Quando algo acontece em uma aplicação, ela "liga" para outra aplicação avisando.

### **4. Containerização**
Cada serviço (Django, PostgreSQL, N8N) roda em um **"container"** isolado, como se fosse um computador separado.

## 🔍 **Pontos de Atenção na Call**

### **1. Por que Docker?**
- **Consistência**: Funciona igual em qualquer ambiente
- **Isolamento**: Cada serviço fica separado
- **Facilidade**: Um comando levanta tudo
- **Portabilidade**: Roda em qualquer lugar

### **2. Por que Django?**
- **Rápido desenvolvimento**: Muitas coisas já prontas
- **Segurança**: CSRF, validação, etc.
- **Admin automático**: Interface para gerenciar dados
- **ORM**: Não precisa escrever SQL

### **3. Por que PostgreSQL?**
- **Confiável**: Usado por grandes empresas
- **Relacional**: Dados organizados
- **ACID**: Garante integridade
- **Gratuito**: Open source

### **4. Por que N8N?**
- **Automação visual**: Fácil de configurar
- **Webhooks**: Recebe dados de outras aplicações
- **Integração**: Conecta com muitos serviços
- **Workflows**: Sequência de ações automáticas

### **5. Como funciona a integração?**
1. Usuário preenche formulário no Django
2. Django valida e salva no PostgreSQL
3. Django envia webhook para N8N
4. N8N recebe, valida e responde
5. Django mostra mensagem de sucesso

## 🎉 **Conclusão**

Este projeto demonstra:
- ✅ **Conhecimento de Docker** e containerização
- ✅ **Desenvolvimento com Django** (MVT, ORM, Admin)
- ✅ **Banco de dados PostgreSQL** e modelagem
- ✅ **Integração com N8N** e webhooks
- ✅ **Testes unitários** e qualidade de código
- ✅ **Configuração via variáveis de ambiente**
- ✅ **Implementação de diferenciais** (busca, paginação, etc.)

O sistema é **funcional, escalável e bem estruturado**, atendendo todos os requisitos obrigatórios e implementando vários diferenciais!
