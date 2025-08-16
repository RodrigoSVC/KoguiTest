#!/bin/bash

# Script de desenvolvimento para o Sistema de Leads

set -e

echo "🚀 Sistema de Leads - Script de Desenvolvimento"
echo "================================================"

case "$1" in
    "start")
        echo "📦 Iniciando o projeto..."
        docker compose up -d --build
        echo "✅ Projeto iniciado!"
        echo "🌐 Acesse: http://localhost:8000"
        echo "🔧 N8N: http://localhost:5678"
        ;;
    
    "stop")
        echo "🛑 Parando o projeto..."
        docker compose down
        echo "✅ Projeto parado!"
        ;;
    
    "restart")
        echo "🔄 Reiniciando o projeto..."
        docker compose down
        docker compose up -d --build
        echo "✅ Projeto reiniciado!"
        ;;
    
    "logs")
        echo "📝 Mostrando logs..."
        docker compose logs -f
        ;;
    
    "migrate")
        echo "🗄️ Executando migrações..."
        docker compose exec challenge_web python manage.py migrate
        echo "✅ Migrações executadas!"
        ;;
    
    "makemigrations")
        echo "📝 Criando migrações..."
        docker compose exec challenge_web python manage.py makemigrations
        echo "✅ Migrações criadas!"
        ;;
    
    "shell")
        echo "🐍 Abrindo shell do Django..."
        docker compose exec challenge_web python manage.py shell
        ;;
    
    "test")
        echo "🧪 Executando testes..."
        docker compose exec challenge_web python manage.py test
        ;;
    
    "format")
        echo "🎨 Formatando código..."
        docker compose exec challenge_web black .
        docker compose exec challenge_web isort .
        echo "✅ Código formatado!"
        ;;
    
    "lint")
        echo "🔍 Verificando código..."
        docker compose exec challenge_web flake8 .
        echo "✅ Verificação concluída!"
        ;;
    
    "superuser")
        echo "👤 Criando superusuário..."
        docker compose exec challenge_web python manage.py createsuperuser
        ;;
    
    "collectstatic")
        echo "📦 Coletando arquivos estáticos..."
        docker compose exec challenge_web python manage.py collectstatic --noinput
        echo "✅ Arquivos estáticos coletados!"
        ;;
    
    "clean")
        echo "🧹 Limpando containers e volumes..."
        docker compose down -v
        docker system prune -f
        echo "✅ Limpeza concluída!"
        ;;
    
    "help"|*)
        echo "📖 Comandos disponíveis:"
        echo "  start         - Inicia o projeto"
        echo "  stop          - Para o projeto"
        echo "  restart       - Reinicia o projeto"
        echo "  logs          - Mostra logs em tempo real"
        echo "  migrate       - Executa migrações"
        echo "  makemigrations- Cria migrações"
        echo "  shell         - Abre shell do Django"
        echo "  test          - Executa testes"
        echo "  format        - Formata código (black + isort)"
        echo "  lint          - Verifica código (flake8)"
        echo "  superuser     - Cria superusuário"
        echo "  collectstatic - Coleta arquivos estáticos"
        echo "  clean         - Limpa containers e volumes"
        echo "  help          - Mostra esta ajuda"
        ;;
esac

