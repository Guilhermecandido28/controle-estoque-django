# forms.py
from django import forms
from clientes.models import Clientes

class VendaForms(forms.Form):    
    cliente = forms.ModelChoiceField(
        queryset=Clientes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),        
    )
    desconto = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control mb-3'}))
    FORMAS_DE_PAGAMENTO = [
        ('CARTAO', 'Cartão de Crédito'),
        ('DEBITO', 'Cartão de Débito'),
        ('DINHEIRO', 'Dinheiro'),
        ('PIX', 'PIX'),
    ]
    
    radio = forms.ChoiceField(choices=FORMAS_DE_PAGAMENTO, widget=forms.RadioSelect)
