from rest_framework import serializers
from estoque.models import Estoque


class EstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estoque
        fields = ['id', 'descricao', 'tamanho', 'cor', 'quantidade', 'venda', 'custo']

