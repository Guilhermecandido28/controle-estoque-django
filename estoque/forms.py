from django import forms
from .models import CategoriaEstoque, MarcaEstoque, Estoque


class AddEstoqueForms(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Estoque
        exclude = ['id','codigo_barras','data', 'imagem']
        widgets = {
            'descricao': forms.TextInput(
                attrs={
                'placeholder': 'Descrição',
                'autofocus': True,
                'id': 'descricao'
                }
                ),
            'tamanho': forms.TextInput(
                attrs={
                'placeholder': 'Tamanho',
                'id': 'tamanho'
                }
                ),
            'cor': forms.TextInput(
                attrs={
                'placeholder': 'cor',
                'id': 'cor'
                      }
                      ),
            'quantidade': forms.NumberInput(
                attrs={
                'id': 'quantidade'
                }),
            'fornecedor': forms.TextInput(
                attrs={
                'placeholder': 'Fornecedor',
                'id': 'fornecedor'}),
            'categoria_id': forms.ModelChoiceField(queryset=CategoriaEstoque.objects.all(), empty_label=None, widget=forms.Select(attrs={'id': 'categoria'})),  
            'marca_id': forms.ModelChoiceField(queryset=MarcaEstoque.objects.all(), empty_label=None, widget=forms.Select(attrs={'id': 'marca'})),  
            'estoque_minimo': forms.NumberInput(attrs={'id':'estoque_min'}),
            'observacoes': forms.TextInput(attrs={'placeholder': 'Observações', 'id': 'obs'}),
        }
        labels = {
            'descricao': 'Descrição:',
            'tamanho': 'Tamanho:',
            'cor': 'Cor:',
            'quantidade': 'Quantidade:',
            'estoque_minimo': 'Estoque Mínimo:',
            'observacoes': 'Observações:',
            'fornecedor': 'Fornecedor:',
            'venda': 'Venda:',
            'categoria_id': 'Categoria:',
            'marca_id': 'Marca:',
            'custo' : 'Custo:',
        }

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        return descricao.title()
    
    def clean_tamanho(self):
        tamanho = self.cleaned_data['tamanho']
        return tamanho.upper()
    
    def clean_cor(self):
        cor = self.cleaned_data['cor']
        return cor.title()
    
    def clean_fornecedor(self):
        fornecedor = self.cleaned_data['fornecedor']
        return fornecedor.title()

    def __init__(self, *args, **kwargs):
        super(AddEstoqueForms, self).__init__(*args, **kwargs)
        self.fields['venda'].widget.attrs['id'] = 'venda'
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})



class EditarForm(forms.ModelForm):
    required_css_class = 'required' 


    categoria = forms.ModelChoiceField(queryset=CategoriaEstoque.objects.all(), empty_label=None)
    marca = forms.ModelChoiceField(queryset=MarcaEstoque.objects.all(), empty_label=None)

    class Meta:
        model = Estoque
        fields = ('descricao', 'tamanho', 'cor', 'quantidade', 'fornecedor', 'venda')
        

    def __init__(self, *args, **kwargs):
        super(EditarForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
    
    def save(self, commit=True):
        # Obtém uma instância do Estoque a ser salvo
        instance = super(EditarForm, self).save(commit=False)

        # Obtém as chaves estrangeiras selecionadas
        categoria = self.cleaned_data['categoria']
        marca = self.cleaned_data['marca']

        # Atribui as chaves estrangeiras à instância do Estoque
        instance.categoria = categoria
        instance.marca = marca

        # Salva a instância do Estoque se commit for True
        if commit:
            instance.save()
        return instance


class AddCategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaEstoque
        fields = ('categoria',)
        widgets = {'categoria': forms.TextInput(attrs={'class': 'form-control', 'id':'nova_categoria'})} 

    def __init__(self, *args, **kwargs):
        super(AddCategoriaForm, self).__init__(*args, **kwargs)        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})

class AddMarcaForm(forms.ModelForm):
    class Meta:
        model = MarcaEstoque
        fields = ('marca',)
        widgets = {'marca': forms.TextInput(attrs={'id':'nova_marca'})} 

    def __init__(self, *args, **kwargs):
        super(AddMarcaForm, self).__init__(*args, **kwargs)        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': ' '})