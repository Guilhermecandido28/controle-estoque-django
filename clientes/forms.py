from django import forms
from .models import Clientes

class ClienteForms(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Clientes
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(
                attrs={
                'placeholder': ' ',
                'autofocus': True,
                'id': 'nome'
                    }
                ),
            'telefone': forms.TextInput(
                attrs={
                'placeholder': ' ',
                'autofocus': True,
                'id': 'telefone'
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                'placeholder': ' ',
                'autofocus': True,
                'id': 'email'
                    }
                ),
            'instagram': forms.TextInput(
                attrs={
                'placeholder': ' ',
                'autofocus': True,
                'id': 'instagram'
                    }
                ),
            }
        labels = {
            'nome': 'Nome:',
            'telefone': 'Telefone:',
            'email': 'Email:',
            'instagram': 'Instagram:',            
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome']
        return nome.title()

    def __init__(self, *args, **kwargs):
        super(ClienteForms, self).__init__(*args, **kwargs)        
        for field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})    
    

