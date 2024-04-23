from django.db import models
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
    
    def  __str__(self):
        return self.descricao
