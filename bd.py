import sqlite3
from datetime import datetime

# Conectar ao banco de dados de origem
source_conn = sqlite3.connect('banco.db')
source_cursor = source_conn.cursor()

# Conectar ao banco de dados de destino
destination_conn = sqlite3.connect('db.sqlite3')
destination_cursor = destination_conn.cursor()

# Copiar os dados da tabela 'estoque'
source_cursor.execute("""
SELECT ID, descricao, categoria, marca, estoque_minimo, quantidade, observacoes, tamanho, 
       fornecedor, cor, custo, venda 
FROM estoque;
""")
rows = source_cursor.fetchall()

# Definir uma data qualquer e valor em branco para 'imagem'
default_date = datetime.now().strftime('%Y-%m-%d')  # Exemplo de data atual
default_image = ""  # Valor em branco para 'imagem'

# Modificar as linhas para incluir os valores padrão para 'data', 'imagem' e 'fornecedor'
modified_rows = []
for row in rows:
    row = list(row)  # Convertendo a tupla para lista para facilitar a modificação
    if not row[8]:  # Índice 8 corresponde à coluna 'fornecedor'
        row[8] = "Sem Fornecedor"
    modified_rows.append(tuple(row) + (default_date, default_image))

# Print dos dados que serão copiados (opcional)
print("Dados a serem copiados:")
for row in modified_rows:
    print(row)

# Inserir os dados na tabela 'estoque_estoque'
if modified_rows:  # Verifica se há dados a serem inseridos
    insert_sql = """
    INSERT INTO estoque_estoque 
    (codigo_barras, descricao, categoria_id, marca_id, estoque_minimo, quantidade, 
    observacoes, tamanho, fornecedor, cor, custo, venda, data, imagem) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    destination_cursor.executemany(insert_sql, modified_rows)
    destination_conn.commit()

# Fechar as conexões
source_conn.close()
destination_conn.close()

print("Dados copiados com sucesso!")
