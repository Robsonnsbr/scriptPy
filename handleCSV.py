import csv
import os
import zipfile
from datetime import datetime

# Descompactar o arquivo dados.zip
with zipfile.ZipFile('dados.zip', 'r') as zip_ref:
    zip_ref.extractall('dados')

# Ler o arquivo origem-dados.csv
dados_file = os.path.join('dados', 'origem-dados.csv')
tipos_file = os.path.join('dados', 'tipos.csv')

dados_filtrados = []
tipos = {}

with open(dados_file, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        if row['status'] == 'CRÍTICO':
            dados_filtrados.append(row)

# Ordenar os dados filtrados pelo campo created_at
dados_filtrados = sorted(dados_filtrados, key=lambda x: datetime.strptime(x['created_at'], '%Y-%m-%d'))

# Ler o arquivo tipos.csv
with open(tipos_file, 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        tipos[row['id']] = row['nome']

# Adicionar o campo "nome_tipo" aos dados filtrados
for dado in dados_filtrados:
    dado['nome_tipo'] = tipos.get(dado['id_tipo'])

# Gerar o arquivo insert-dados.sql
sql_file = os.path.join('dados', 'insert-dados.sql')

with open(sql_file, 'w') as sql_file:
    for dado in dados_filtrados:
        sql = "INSERT INTO dados_finais (id, created_at, status, id_tipo, nome_tipo) VALUES ({}, '{}', '{}', {}, '{}');\n".format(
            dado['id'], dado['created_at'], dado['status'], dado['id_tipo'], dado['nome_tipo'])
        sql_file.write(sql)

# Montar a query para obter a quantidade de itens agrupados por tipo, por dia
query = "SELECT created_at::date, nome_tipo, COUNT(*) FROM dados_finais GROUP BY created_at::date, nome_tipo;"

print("Arquivo insert-dados.sql gerado com sucesso.")
print("Query para obter a quantidade de itens agrupados por tipo, por dia:")
print(query)


# # Conectar ao banco de dados MYSQL
# conn = mysql.connector.connect(
#     host="localhost",
#     port=3306,
#     database="dados_python",
#     user="root",
#     password="root"
# )

# # Criar a tabela dados_finais no banco de dados
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS dados_finais (
#   id INT,
#   created_at DATE,
#   status VARCHAR(20),
#   id_tipo INT,
#   nome_tipo VARCHAR(50)
# );
# '''

# with conn.cursor() as cursor:
#     cursor.execute(create_table_query)
#     conn.commit()

# # Inserir os dados na tabela dados_finais
# insert_query = '''
# LOAD DATA INFILE '{}'
# INTO TABLE dados_finais
# FIELDS TERMINATED BY ','
# ENCLOSED BY '"'
# LINES TERMINATED BY '\n'
# IGNORE 1 ROWS;
# '''

# with conn.cursor() as cursor:
#     cursor.execute(insert_query.format(dados_file))
#     conn.commit()
