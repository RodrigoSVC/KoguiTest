import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from .models import Lead
from .forms import LeadForm, LeadEditForm


def dashboard(request):
    total_leads = Lead.objects.count()
    novos_leads = Lead.objects.filter(status='novo').count()
    qualificados = Lead.objects.filter(status='qualificado').count()
    convertidos = Lead.objects.filter(status='convertido').count()
    leads_recentes = Lead.objects.all()[:5]

    context = {
        'total_leads': total_leads,
        'novos_leads': novos_leads,
        'qualificados': qualificados,
        'convertidos': convertidos,
        'leads_recentes': leads_recentes,
    }
    return render(request, 'leads/dashboard.html', context)


def cadastrar_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            try:
                webhook_data = {
                    'nome': lead.nome,
                    'email': lead.email,
                }
                
                webhook_url = settings.N8N_WEBHOOK_URL
                auth = (settings.N8N_USER, settings.N8N_PASSWORD)
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'User-Agent': 'Django-Leads-System/1.0'
                }
                
                response = requests.post(
                    webhook_url,
                    json=webhook_data,
                    auth=auth,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        if response_data.get('ok', False):
                            messages.success(request, 'Lead cadastrado com sucesso!')
                        else:
                            messages.success(request, 'Lead cadastrado com sucesso!')
                    except:
                        messages.success(request, 'Lead cadastrado com sucesso!')
                else:
                    messages.warning(request, f'Lead cadastrado, mas N8N retornou status {response.status_code}')
                    
            except Exception as e:
                messages.warning(request, f'Lead cadastrado, mas erro ao enviar webhook: {str(e)}')
            
            return redirect('leads:dashboard')
    else:
        form = LeadForm()

    return render(request, 'leads/cadastrar_lead.html', {'form': form})


def lista_leads(request):
    leads_list = Lead.objects.all()
    
    query = request.GET.get('q')
    if query:
        leads_list = leads_list.filter(
            Q(nome__icontains=query) |
            Q(email__icontains=query) |
            Q(empresa__icontains=query)
        )
    
    paginator = Paginator(leads_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'leads/lista_leads.html', context)


def visualizar_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    return render(request, 'leads/visualizar_lead.html', {'lead': lead})


def editar_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == 'POST':
        form = LeadEditForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lead atualizado com sucesso!')
            return redirect('leads:lista_leads')
    else:
        form = LeadEditForm(instance=lead)
    
    return render(request, 'leads/editar_lead.html', {'form': form, 'lead': lead})


def excluir_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == 'POST':
        lead.delete()
        messages.success(request, 'Lead excluído com sucesso!')
        return redirect('leads:lista_leads')
    
    return render(request, 'leads/excluir_lead.html', {'lead': lead})

