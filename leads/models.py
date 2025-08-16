from django.db import models


class Lead(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo'),
        ('contatado', 'Contatado'),
        ('qualificado', 'Qualificado'),
        ('convertido', 'Convertido'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name='Nome Completo')
    email = models.EmailField(verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    empresa = models.CharField(max_length=200, blank=True, null=True, verbose_name='Empresa')
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cargo')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='novo', verbose_name='Status')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome} - {self.empresa or 'Sem empresa'}"

    @property
    def nome_curto(self):
        return self.nome.split()[0] if self.nome else ''

