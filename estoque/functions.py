import random
from reportlab.lib.units import mm
from PIL import Image
from barcode import EAN13
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
from io import BytesIO
import os

def gerar_ean13():
    # Gere os primeiros 11 dígitos, excluindo o primeiro dígito
    doze_numeros = ''.join([str(random.randint(0,9)) for i in range(11)])
    
    # Adicione um dígito aleatório diferente de zero como primeiro dígito
    primeiro_digito = str(random.randint(1,9))
    ean13 = primeiro_digito + doze_numeros
    
    # Calcule o último dígito de verificação
    pares = sum(int(p) for p in ean13[::2])
    impares = sum(int(im) for im in ean13[1::2])
    soma_total = pares + impares * 3
    digito = (10 - (soma_total % 10)) % 10
    
    # Adicione o último dígito de verificação ao código de barras
    ean13 += str(digito)
    
    return ean13





def criar_etiqueta(codigo_barras, preco, tamanho):
    buf = BytesIO()
    # Configurações do documento
    c = canvas.Canvas(buf, pagesize=(40 * mm, 40 * mm))

    # Dimensões da etiqueta (40x40 mm)
    largura_etiqueta = 40 * mm
    altura_etiqueta = 40 * mm

    # Gerar o código de barras no padrão EAN-13 usando python-barcode
    barcode_buf = BytesIO()
    ean = EAN13(codigo_barras, writer=ImageWriter())
    ean.write(barcode_buf)

    # Abrir a imagem do código de barras sem redimensionar
    barcode_buf.seek(0)
    barcode_image = Image.open(barcode_buf)

    # Salvar a imagem do código de barras em um caminho temporário
    temp_img_path = "temp_barcode_image.png"
    barcode_image.save(temp_img_path)

    # Adicionar a imagem do código de barras ao canvas sem redimensionamento
    c.drawImage(temp_img_path, largura_etiqueta * 0.05, altura_etiqueta * 0.4, width=largura_etiqueta * 0.9, height=altura_etiqueta * 0.5)

    # Adicionar o preço abaixo do código de barras e centralizado
    c.setFont("Helvetica", 18)
    
    # Calcular a largura do texto do preço
    preco_texto = preco
    preco_width = c.stringWidth(preco_texto, "Helvetica", 18)
    
    # Calcular a posição para centralizar o preço
    preco_x = (largura_etiqueta - preco_width) / 2
    preco_y = altura_etiqueta * 0.2  # Ajustar a posição vertical conforme necessário
    
    c.drawString(preco_x, preco_y, preco_texto)

    # Texto do tamanho
    tamanho_texto = f"TAM: {tamanho}"
    tamanho_width = c.stringWidth(tamanho_texto, "Helvetica", 18)
    
    # Calcular a posição para centralizar o tamanho
    tamanho_x = (largura_etiqueta - tamanho_width) / 2
    tamanho_y = preco_y - 18  # Ajustar a posição vertical para ficar abaixo do preço
    
    c.drawString(tamanho_x, tamanho_y, tamanho_texto)

    # Finalizar o PDF
    c.save()
    buf.seek(0)

    # Remover o arquivo temporário após a criação do PDF
    os.remove(temp_img_path)

    return buf



