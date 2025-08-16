from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('cadastrar/', views.cadastrar_lead, name='cadastrar_lead'),
    path('lista/', views.lista_leads, name='lista_leads'),
    path('visualizar/<int:lead_id>/', views.visualizar_lead, name='visualizar_lead'),
    path('editar/<int:lead_id>/', views.editar_lead, name='editar_lead'),
    path('excluir/<int:lead_id>/', views.excluir_lead, name='excluir_lead'),
]

