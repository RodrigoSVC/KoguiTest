from django.test import TestCase, Client
from django.urls import reverse
from .models import Lead
from .forms import LeadForm


class LeadModelTest(TestCase):
    def setUp(self):
        self.lead = Lead.objects.create(
            nome="João Silva",
            email="joao@teste.com",
            empresa="Empresa Teste",
            telefone="(11) 99999-9999"
        )

    def test_lead_creation(self):
        self.assertEqual(self.lead.nome, "João Silva")
        self.assertEqual(self.lead.email, "joao@teste.com")
        self.assertEqual(self.lead.status, "novo")

    def test_lead_str_representation(self):
        expected = "João Silva - Empresa Teste"
        self.assertEqual(str(self.lead), expected)

    def test_lead_nome_curto_property(self):
        self.assertEqual(self.lead.nome_curto, "João")


class LeadFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'nome': 'Maria Santos',
            'email': 'maria@teste.com',
            'empresa': 'Empresa Teste'
        }
        form = LeadForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_required_fields(self):
        form_data = {
            'empresa': 'Empresa Teste'
        }
        form = LeadForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nome', form.errors)
        self.assertIn('email', form.errors)

    def test_invalid_email_format(self):
        form_data = {
            'nome': 'João Silva',
            'email': 'email-invalido',
            'empresa': 'Empresa Teste'
        }
        form = LeadForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)


class LeadViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.lead = Lead.objects.create(
            nome="João Silva",
            email="joao@teste.com",
            empresa="Empresa Teste"
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('leads:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/dashboard.html')

    def test_lista_leads_view(self):
        response = self.client.get(reverse('leads:lista_leads'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/lista_leads.html')

    def test_cadastrar_lead_view_get(self):
        response = self.client.get(reverse('leads:cadastrar_lead'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/cadastrar_lead.html')

    def test_cadastrar_lead_view_post_valid(self):
        form_data = {
            'nome': 'Maria Santos',
            'email': 'maria@teste.com',
            'empresa': 'Empresa Teste'
        }
        response = self.client.post(reverse('leads:cadastrar_lead'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Lead.objects.filter(email='maria@teste.com').exists())

    def test_visualizar_lead_view(self):
        response = self.client.get(reverse('leads:visualizar_lead', args=[self.lead.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/visualizar_lead.html')

    def test_editar_lead_view_get(self):
        response = self.client.get(reverse('leads:editar_lead', args=[self.lead.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/editar_lead.html')

    def test_excluir_lead_view_get(self):
        response = self.client.get(reverse('leads:excluir_lead', args=[self.lead.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/excluir_lead.html')

    def test_excluir_lead_view_post(self):
        response = self.client.post(reverse('leads:excluir_lead', args=[self.lead.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Lead.objects.filter(id=self.lead.id).exists())


class LeadURLsTest(TestCase):
    def test_dashboard_url(self):
        url = reverse('leads:dashboard')
        self.assertEqual(url, '/')

    def test_cadastrar_lead_url(self):
        url = reverse('leads:cadastrar_lead')
        self.assertEqual(url, '/cadastrar/')

    def test_lista_leads_url(self):
        url = reverse('leads:lista_leads')
        self.assertEqual(url, '/lista/')

    def test_visualizar_lead_url(self):
        url = reverse('leads:visualizar_lead', args=[1])
        self.assertEqual(url, '/visualizar/1/')

    def test_editar_lead_url(self):
        url = reverse('leads:editar_lead', args=[1])
        self.assertEqual(url, '/editar/1/')

    def test_excluir_lead_url(self):
        url = reverse('leads:excluir_lead', args=[1])
        self.assertEqual(url, '/excluir/1/')


class LeadSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        Lead.objects.create(nome="João Silva", email="joao@teste.com", empresa="Empresa A")
        Lead.objects.create(nome="Maria Santos", email="maria@teste.com", empresa="Empresa B")
        Lead.objects.create(nome="Pedro Costa", email="pedro@teste.com", empresa="Empresa C")

    def test_search_by_name(self):
        response = self.client.get(reverse('leads:lista_leads'), {'q': 'João'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')
        self.assertNotContains(response, 'Maria Santos')

    def test_search_by_email(self):
        response = self.client.get(reverse('leads:lista_leads'), {'q': 'maria@teste.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Santos')
        self.assertNotContains(response, 'João Silva')

    def test_search_by_company(self):
        response = self.client.get(reverse('leads:lista_leads'), {'q': 'Empresa A'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'João Silva')
        self.assertNotContains(response, 'Maria Santos')

