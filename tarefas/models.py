from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from vendedores.models import Vendedores
from datetime import datetime
import calendar

class Tarefas(models.Model):
    periodicidade = [
        ('1', 'Diária'),
        ('2', 'Semanal'),
        ('3', 'Mensal'),
        ('4', 'Dias alternados')
    ]

    id = models.AutoField(primary_key=True)
    tarefa = models.TextField()
    inicio = models.DateTimeField(default=timezone.now)
    prazo = models.DateTimeField(default= timezone.now)
    status = models.BooleanField(default=False)
    funcionario = models.ForeignKey(Vendedores, on_delete=models.CASCADE, default=1)
    cor = models.CharField(max_length=10, null=True, blank=True)
    recorrencia  = models.CharField(max_length=50, choices=periodicidade) 

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'

    def clean(self):
        if self.inicio > self.prazo:
            raise ValidationError("A data de início não pode ser posterior ao prazo.")
        
    def ultimo_dia_do_mes_atual(self):
        hoje = datetime.today()
        ano = hoje.year
        mes = hoje.month
        _, ultimo_dia = calendar.monthrange(ano, mes)
        return datetime(ano, mes, ultimo_dia)

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.status:
            self.cor = 'green'
        else:
            self.cor = 'red'


        if self.recorrencia == '1':
            self.prazo = str(self.ultimo_dia_do_mes_atual())
            
        super().save(*args, **kwargs)    


    def __str__(self):
        return self.tarefa
