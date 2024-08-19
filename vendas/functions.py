from estoque.models import Estoque
from django.http import JsonResponse

def ajustar_estoque(lista):
    for item in lista:
        codigo_barras = item['codigo_barras']
        estoque_item = Estoque.objects.filter(codigo_barras=codigo_barras).first()
        if estoque_item:
            estoque_item.quantidade -= 1
            estoque_item.save()
        else:
            print(f"O item com código de barras {codigo_barras} não está presente no estoque.")
