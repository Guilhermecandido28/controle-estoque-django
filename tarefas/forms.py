from django import forms
from .models import Tarefas


class TarefasForms(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Tarefas
        exclude = ['status', 'id', 'cor']
        widgets = {
            'tarefa': forms.Textarea(
                attrs={
                    'class': 'form-control mb-0',
                    'placeholder': 'Tarefa',
                    'cols': 80,
                    'rows': 20,
                    'autofocus': True,
                    'id': 'tarefas'
                }
            ),
            'inicio': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'Inicio',
                    'id': 'inicio'
                }
            ), 
            'prazo': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'Fim',
                    'id': 'fim'
                }
            ),
            'funcionario': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Funcionário',
                    'id': 'funcionario'
                }
            )             
        }
        labels = {
            'tarefa': 'Tarefas:',
            'inicio': 'Início:',
            'prazo': 'Término',
            'funcionario': 'Funcionário Responsável:',            
        }

    def clean(self):
        cleaned_data = super().clean()
        inicio = cleaned_data.get('inicio')
        prazo = cleaned_data.get('prazo')
        
        if inicio and prazo:
            if inicio > prazo:
                raise forms.ValidationError("A data de início não pode ser posterior ao prazo.")
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

