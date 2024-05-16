from django.db import models
from django.db.models import F
from datetime import datetime
from clientes.models import Clientes

class Vendas(models.Model):
    FORMAS_DE_PAGAMENTO = [
        ('CARTAO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
        ('DINHEIRO', 'Dinheiro'),        
        ('PIX', 'PIX'),
    ]    
    id = models.AutoField(primary_key=True, unique=True) 
    descricao = models.CharField(max_length=1300, default='', null=False, blank=False)
    cliente = models.ForeignKey(Clientes, on_delete=models.SET_NULL, default=None, null=True)
    desconto = models.IntegerField(default=0)        
    forma_pagamento = models.CharField(max_length=50, choices=FORMAS_DE_PAGAMENTO)
    total = models.DecimalField(max_digits=20, decimal_places=2, default = 1)    
    data = models.DateField(default=datetime.now)
    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
    def  __str__(self):
        return self.descricao

    def save(self, *args, **kwargs):
        # Verifica se o cliente está vazio ou não existe
        if self.cliente_id is None or not Clientes.objects.filter(pk=self.cliente_id).exists():
            # Se estiver vazio ou não existir, defina como None
            self.cliente = None

        super().save(*args, **kwargs)

class Caixa(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    data = models.DateField(default=datetime.now)
    valor_inicial = models.DecimalField(max_digits=6, decimal_places=2, default= 0)
    saida = models.DecimalField(max_digits=6, decimal_places=2, default= 0, blank=True, null=True)
    def saldo(self):
        if self.saida is not None:
            return self.valor_inicial - self.saida
        else:
            return self.valor_inicial

    def __str__(self):
        return f'Caixa do dia {self.data} fechou em {self.saldo}'