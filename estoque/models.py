from django.db import models
from datetime import datetime
from .functions import gerar_ean13



class CategoriaEstoque(models.Model):
    id = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.categoria
    
class MarcaEstoque(models.Model):
    id = models.AutoField(primary_key=True)
    marca = models.CharField(max_length = 50, unique=True)

    def __str__(self):
        return self.marca    

    
class Estoque(models.Model):    
    id = models.AutoField(primary_key=True, unique=True)
    codigo_barras = models.CharField(max_length = 14, default = gerar_ean13, unique=True) 
    descricao = models.CharField(max_length=200, default='')
    categoria = models.ForeignKey(CategoriaEstoque, on_delete=models.CASCADE)
    marca = models.ForeignKey(MarcaEstoque, on_delete=models.CASCADE)
    estoque_minimo = models.IntegerField(default=1)
    quantidade = models.IntegerField(default=1)
    observacoes = models.CharField(max_length = 500,  null=True, blank=True)    
    tamanho = models.CharField(max_length = 5, default= 'M')
    fornecedor = models.CharField(max_length = 200, default = 'Sem fornecedor')
    cor = models.CharField(max_length = 200, default= "")
    custo = models.DecimalField(max_digits=20, decimal_places=2, default = 1)
    venda = models.DecimalField(max_digits=20, decimal_places=2, default = 1)
    imagem = models.BinaryField(null=True, blank=True)
    data = models.DateField(default=datetime.now)


    
    def  __str__(self):
        return self.descricao
    

    def save(self, *args, **kwargs):
        # Verificar se já existe um Estoque com o mesmo código de barras
        if not self.pk and not self.codigo_barras:
            # Se é uma nova instância e ainda não tem código de barras, gerar um
            self.codigo_barras = gerar_ean13()
        elif not self.pk:
            # Se é uma nova instância e já tem código de barras, verificar se já existe no banco de dados
            while Estoque.objects.filter(codigo_barras=self.codigo_barras).exists():
                self.codigo_barras = gerar_ean13()  # Gerar um novo código de barras único
        
        self.custo = float(self.venda)*0.5

        super().save(*args, **kwargs)

