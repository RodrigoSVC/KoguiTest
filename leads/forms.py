from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nome', 'email', 'telefone', 'empresa', 'cargo', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do lead',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com',
                'required': True
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo na empresa'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações sobre o lead...',
                'rows': 3
            }),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome.strip()) < 2:
            raise forms.ValidationError('O nome deve ter pelo menos 2 caracteres.')
        return nome.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            if Lead.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Este e-mail já está cadastrado.')
        else:
            if Lead.objects.filter(email=email).exists():
                raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email.lower()


class LeadEditForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['nome', 'email', 'telefone', 'empresa', 'cargo', 'status', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do lead',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@empresa.com',
                'required': True
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'empresa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da empresa'
            }),
            'cargo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cargo na empresa'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observações sobre o lead...',
                'rows': 3
            }),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome.strip()) < 2:
            raise forms.ValidationError('O nome deve ter pelo menos 2 caracteres.')
        return nome.strip()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and self.instance.pk:
            if Lead.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Este e-mail já está cadastrado.')
        else:
            if Lead.objects.filter(email=email).exists():
                raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email.lower()

