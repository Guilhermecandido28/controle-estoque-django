from django import forms
from django.contrib import messages

class LoginForms(forms.Form):
    nome_login = forms.CharField(
        label='',
        required= True,
        max_length=100,
        widget=forms.TextInput(
            attrs= {
                'class': "box",
                "placeholder": 'Usuário'
            }
        )
    )
    senha=forms.CharField(
        label='',
        required= True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs= {
                'class': "box",
                "placeholder": 'Senha'
            }
        )
    )

class CadastroForms(forms.Form):
    nome_cadastro = forms.CharField(
        label='',
        required= True,
        max_length=100,
        widget=forms.TextInput(
            attrs= {
                'class': "box",
                "placeholder": 'Usuário'
            }
        )
    )

    email = forms.EmailField(
        label='',
        required= True,
        max_length=100,
        widget=forms.EmailInput(
            attrs= {
                'class': "box",
                "placeholder": 'Email'
            }
        )
    )

    senha_1=forms.CharField(
        label='',
        required= True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs= {
                'class': "box",
                "placeholder": 'Senha',
                "id":"senha"
            }
        )
    )

    senha_2=forms.CharField(
        label='',
        required= True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs= {
                'class': "box",
                "placeholder": 'Confirme a senha',
                "id": 'repetir-senha'
            }
        )
    )

    def clean_nome_cadastro(self):
        nome = self.cleaned_data.get('nome_cadastro')
        if nome:
            nome = nome.strip()
            if " " in nome:                
                raise  forms.ValidationError("Usuário não pode conter espaços")
            else:
                return nome

    def clean_senha_2(self):
        senha_1 = self.cleaned_data.get('senha_1')
        senha_2 = self.cleaned_data.get('senha_2')

        if senha_1 and senha_2:
            if senha_1 != senha_2:
                raise forms.ValidationError("As senhas devem ser iguais.")
            else:
                return senha_2

