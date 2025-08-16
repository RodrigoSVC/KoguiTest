from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'empresa', 'status', 'criado_em']
    list_filter = ['status', 'criado_em']
    search_fields = ['nome', 'email', 'empresa']
    readonly_fields = ['criado_em', 'atualizado_em']
    list_per_page = 20
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'telefone')
        }),
        ('Informações Profissionais', {
            'fields': ('empresa', 'cargo', 'status')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Datas', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )

