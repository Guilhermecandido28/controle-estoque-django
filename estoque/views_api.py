from rest_framework import viewsets
from estoque.models import Estoque
from .serializer import EstoqueSerializer
from rest_framework.pagination import PageNumberPagination


class Paginacao(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
class EstoquesViewSet(viewsets.ModelViewSet):
    """Exibindo todos os produtos do estoque"""
    queryset = Estoque.objects.all().order_by('id')
    serializer_class = EstoqueSerializer
    # pagination_class = Paginacao