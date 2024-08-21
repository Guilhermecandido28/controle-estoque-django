from django.db import models
from django.utils import timezone

class Vendedores(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    foto = models.ImageField(default="https://xsgames.co/randomusers/avatar.php?g=pixel")
    salario = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    total_em_vendas = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    comissao = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    porcentegem_comissao = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    ferias = models.DateField(default= timezone.now)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'       

    def __str__(self):
        return self.nome
    

class EventoVenda(models.Model):
    vendedor = models.ForeignKey(Vendedores, on_delete=models.DO_NOTHING)
    data = models.DateTimeField(default=timezone.now)
    produto = models.CharField(max_length=500)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Evento de Venda'
        verbose_name_plural = 'Eventos de Vendas'

    def __str__(self) -> str:        
        return self.produto
    


