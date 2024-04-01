from django.test import TestCase

from django.test import TestCase
from estoque.models import Estoque, CategoriaEstoque, MarcaEstoque

class EstoqueTestCase(TestCase):
    
    def setUp(self):
        # Criação de objetos CategoriaEstoque e MarcaEstoque
        self.categoria = CategoriaEstoque.objects.create(categoria="Categoria de Teste")
        self.marca = MarcaEstoque.objects.create(marca="Marca de Teste")
        
    def test_codigo_barras_starting_with_zero(self):
        # Criação de um objeto Estoque com um código de barras iniciando com 0
        estoque = Estoque.objects.create(
            descricao="Produto Teste",
            categoria=self.categoria,
            marca=self.marca,
            estoque_minimo=10,
            quantidade=20,
            custo="10.00",
            venda="20.00",
            codigo_barras="0123456789123"  # Código de barras iniciando com 0
        )
        
        # Verificação se o código de barras foi criado corretamente
        self.assertEqual(estoque.codigo_barras, "0123456789123")

    def test_generate_unique_barcode(self):
        # Verifica se o método de gerar código de barras único funciona corretamente
        estoque1 = Estoque.objects.create(
            codigo_barras = '1123456789123',
            descricao="Produto Teste 1",
            categoria=self.categoria,
            marca=self.marca,
            estoque_minimo=10,
            quantidade=20,
            custo="10.00",
            venda="20.00"
        )

        estoque2 = Estoque.objects.create(
            codigo_barras = '1123456789123',
            descricao="Produto Teste 2",
            categoria=self.categoria,
            marca=self.marca,
            estoque_minimo=10,
            quantidade=20,
            custo="10.00",
            venda="20.00"
        )

        self.assertNotEqual(estoque1.codigo_barras, estoque2.codigo_barras)
