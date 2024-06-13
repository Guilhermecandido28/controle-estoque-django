from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from vendedores.models import Vendedores

class Tarefas(models.Model):
    id = models.AutoField(primary_key=True)
    tarefa = models.TextField()
    inicio = models.DateTimeField(default=timezone.now)
    prazo = models.DateTimeField(default= timezone.now)
    status = models.BooleanField(default=True)
    funcionario = models.ForeignKey(Vendedores, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'       
    
    def clean(self):
        if self.inicio > self.prazo:
            raise ValidationError("A data de início não pode ser posterior ao prazo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tarefa
