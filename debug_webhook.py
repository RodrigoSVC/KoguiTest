#!/usr/bin/env python3
"""
Script para debugar o webhook com dados reais do Django
"""

import requests
import json
from datetime import datetime

# URL do webhook
webhook_url = "https://drikydev.app.n8n.cloud/webhook/webhook/lead-received"

# Dados EXATOS que o Django está enviando (com encoding)
test_data = {
    "id": 1,
    "nome": "Joao Silva",  # Sem acentos
    "email": "joao@teste.com",
    "empresa": "Empresa Teste",
    "telefone": "(11) 99999-9999",
    "cargo": "Desenvolvedor",
    "status": "novo",
    "criado_em": datetime.now().isoformat()
}

print("🔍 DEBUG: Testando webhook com dados reais...")
print(f"URL: {webhook_url}")
print(f"Dados enviados: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
print("-" * 50)

try:
    # Configurar autenticação básica
    auth = ('admin', 'admin123')
    
    # Enviar requisição
    response = requests.post(
        webhook_url,
        json=test_data,
        auth=auth,
        timeout=10,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📄 Response Headers: {dict(response.headers)}")
    print(f"📝 Response Body: {response.text}")
    
    # Analisar a resposta
    try:
        response_json = response.json()
        print(f"🔍 Resposta JSON: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
        
        if response_json.get('ok', False):
            print("🎉 SUCESSO: N8N validou os dados corretamente!")
        else:
            print(f"⚠️  ERRO: N8N rejeitou os dados: {response_json.get('message', 'Erro desconhecido')}")
            
    except json.JSONDecodeError:
        print("⚠️  Resposta não é JSON válido")
        
except Exception as e:
    print(f"❌ Erro inesperado: {str(e)}")
