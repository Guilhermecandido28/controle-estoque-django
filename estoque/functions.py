import random

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

