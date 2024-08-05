# forms.py
from django import forms
from clientes.models import Clientes
from .models import Caixa, Vendas, Troca
from vendedores.models import Vendedores
from estoque.models import Estoque


class VendaForms(forms.Form):    
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),        
    )
    
    data = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    vendedor = forms.ModelChoiceField(queryset=Vendedores.objects.all(), empty_label="Selecione um Vendedor(a)", widget=forms.Select(attrs={'class': 'form-control mb-3'}))
    FORMAS_DE_PAGAMENTO = [
        ('CARTAO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
    ]
    
    radio = forms.ChoiceField(choices=FORMAS_DE_PAGAMENTO, widget=forms.RadioSelect)
    

class CaixaForms(forms.ModelForm):
    class Meta:
        model = Caixa
        fields = ['valor_inicial', 'saida']  # Lista dos campos do modelo que deseja incluir no formulário
        widgets = {
            'valor_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' ', 'id': 'valor_inicial'}),
            'saida': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' ', 'id': 'saidas'})
        }
        labels = {
            'valor_inicial': 'Valor Inicial',
            'saida': 'Saídas'
        }

class TrocaForms(forms.ModelForm):
    class Meta:
        model = Troca
        fields = ['produto_trocado', 'produto_novo']
        widgets = {
            'produto_trocado' : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': ' ',
                    'id': 'produto_trocado',
                    'hx-post': 'produto_trocado/',
                    'hx-target': '#info_produto_trocado',
                    'hx-swap': 'innerHTML',
                    'hx-trigger': 'keyup'
                }
            ),
            'produto_novo' : forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': ' ',
                    'id': 'produto_novo',
                    'hx-post': 'produto_novo/',
                    'hx-target': '#info_produto_novo',
                    'hx-swap': 'innerHTML',
                    'hx-trigger': 'keyup'
                }
            ),            
        }