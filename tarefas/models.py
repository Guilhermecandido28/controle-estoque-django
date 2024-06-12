from django.db import models
from django.utils import timezone

class Tarefas(models.Model):
    id = models.AutoField(primary_key=True)
    tarefa = models.CharField(max_length=50)
    inicio = models.DateField(default=timezone.now)
    prazo = models.DateField(default= timezone.now)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'       

    def __str__(self):
        return self.tarefa
