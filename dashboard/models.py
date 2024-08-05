from django.db import models

class Saidas(models.Model):
    STATUS = [
        ('C', 'CONCLUÍDO'),
        ('P', 'PENDENTE'),
    ]
    data = models.DateField()
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.descricao

