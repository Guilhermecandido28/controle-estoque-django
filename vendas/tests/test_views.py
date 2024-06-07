# In your_app/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, datetime
from decimal import Decimal
from vendas.models import Vendas, Caixa
from estoque.models import Estoque, CategoriaEstoque, MarcaEstoque
from clientes.models import Clientes
from vendedores.models import Vendedores


lista_preco=[]
class VendaViewTests(TestCase):
    def setUp(self):
        # Setting up the client and necessary data
        self.client = Client()
        
        # Create necessary objects for the tests
        self.vendedor = Vendedores.objects.create(nome="Test Vendedor")
        self.cliente = Clientes.objects.create(nome="Test Cliente")
        self.categoria = CategoriaEstoque.objects.create(categoria = 'camiseta')
        self.marca = MarcaEstoque.objects.create(marca = 'teste')
        self.produto = Estoque.objects.create(
            codigo_barras="1234567890123",
            descricao="Test Item",
            tamanho="M",
            categoria_id = '1',
            marca_id = '1',
            cor="Red",
            venda=Decimal("10.00")
        )
        self.caixa = Caixa.objects.create(data=date.today(), valor_inicial=Decimal("100.00"))

    def test_venda_view_get(self):
        # Test GET request on venda view
        response = self.client.get(reverse('venda'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vendas/venda.html')

    # def test_inserir_venda_post(self):
    #     # Test POST request on inserir_venda
    #     data = {
    #         'codigo_barras': '1234567890123',
    #         'quantidade': 2
    #     }
    #     response = self.client.post(reverse('inserir_venda'), data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'vendas/partials/_table.html')
    #     self.assertIn('Test Item', response.content.decode())

    # def test_salvar_venda_post(self):
    #     # Test POST request on salvar_venda
    #     lista_preco.append({
    #         'codigo_barras': '1234567890123',
    #         'descricao': 'Test Item',
    #         'tamanho': 'M',
    #         'cor': 'Red',
    #         'venda': Decimal('10.00'),
    #         'total': Decimal('20.00')
    #     })
    #     data = {
    #         'vendedor': self.vendedor.id,
    #         'cliente': self.cliente.id,
    #         'desconto': '10',
    #         'radio': 'cash'
    #     }
    #     response = self.client.post(reverse('salvar_venda'), data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'vendas/partials/_message.html')
    #     self.assertTrue(Vendas.objects.filter(cliente=self.cliente).exists())

    # def test_movimentacao_dia(self):
    #     # Test movimentacao_dia view
    #     Vendas.objects.create(
    #         descricao="Test Item; M; Red",
    #         cliente=self.cliente,
    #         desconto=Decimal('10.00'),
    #         forma_pagamento='cash',
    #         data=date.today(),
    #         total=Decimal('18.00'),
    #         vendedor=self.vendedor
    #     )
    #     response = self.client.get(reverse('movimentacao_dia'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'cash')
    #     self.assertContains(response, '18.00')

    # def test_caixa_valor_inicial_post(self):
    #     # Test POST request on caixa_valor_inicial
    #     data = {'valor_inicial': '200.00'}
    #     response = self.client.post(reverse('caixa_valor_inicial'), data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'vendas/partials/caixa_valor_inicial.html')
    #     self.assertTrue(Caixa.objects.filter(valor_inicial=Decimal('200.00')).exists())

    # def test_caixa_lancar_saida_post(self):
    #     # Test POST request on caixa_lancar_saida
    #     data = {'saida': '50.00'}
    #     response = self.client.post(reverse('caixa_lancar_saida'), data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'vendas/partials/caixa_valor_inicial.html')
    #     self.caixa.refresh_from_db()
    #     self.assertEqual(self.caixa.saida, Decimal('50.00'))

    # def test_pesquisar_vendas_post(self):
    #     # Test POST request on pesquisar_vendas
    #     Vendas.objects.create(
    #         descricao="Test Item; M; Red",
    #         cliente=self.cliente,
    #         desconto=Decimal('10.00'),
    #         forma_pagamento='cash',
    #         data=date.today(),
    #         total=Decimal('18.00'),
    #         vendedor=self.vendedor
    #     )
    #     response = self.client.post(reverse('pesquisar_vendas'), {})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'vendas/partials/_table_vendas.html')
    #     self.assertContains(response, 'Test Cliente')
