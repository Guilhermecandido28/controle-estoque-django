from django import forms
from .models import Saidas

class SaidaForms(forms.ModelForm):
    class Meta:
        model = Saidas
        fields = '__all__'  # Lista dos campos do modelo que deseja incluir no formulário
        widgets = {
            'data': forms.DateTimeInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Data',
                    'id': 'data'
                }
            ), 
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' ', 'id': 'descricao'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' ',}),
        }            
        labels = {
            'data': 'Data',
            'descricao': 'Descrição',
            'valor': 'Valor',
            
        }