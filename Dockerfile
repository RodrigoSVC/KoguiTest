# Multi-stage build para otimizar a imagem
FROM python:3.11-slim as builder

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Stage de produção
FROM python:3.11-slim

# Instalar curl para healthcheck
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências do stage anterior
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiar código da aplicação
COPY . .

# Criar diretório para arquivos estáticos
RUN mkdir -p /app/staticfiles

# Coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

# Mudar propriedade dos arquivos para o usuário app
RUN chown -R app:app /app

# Mudar para usuário não-root
USER app

# Expor porta
EXPOSE 8000

# Comando para executar a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

