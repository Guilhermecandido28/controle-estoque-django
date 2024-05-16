from django.db import models


class Vendedores(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    foto = models.ImageField(default="https://xsgames.co/randomusers/avatar.php?g=pixel")
    salario = models.DecimalField(max_digits=6, decimal_places=2, default=1)
    produtos_vendidos = models.IntegerField(default=0)
    comissao = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    ferias = models.DateField(default= 'django.utils.timezone.now')

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'       

    def __str__(self):
        return self.nome
    


    
