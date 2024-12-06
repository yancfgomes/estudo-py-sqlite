# importa a biblioteca sqlite3
import sqlite3

# importa a biblioteca pathlib para manipulação de
# caminhos de arquivos e diretórios
from pathlib import Path

# Define a variável ROOT_PATH que recebe
# o caminho do diretório pai do arquivo atual
ROOT_PATH = Path(__file__).parent

# Conecta ao banco de dados
connection = sqlite3.connect(ROOT_PATH/"my-database.db")

# Cria um cursor para manipular o banco de dados
# Cursor: objeto que permite executar comandos SQL
cursor = connection.cursor()

# Função para criar a tabela clientes


def create_table(connection, cursor):
    cursor.execute('''
        CREATE TABLE clients(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100),
            email VARCHAR(150)
        )
    ''')
    connection.commit()

# Função para inserir um registro na tabela clientes


def insert(connection, cursor, name, email):
    data = (name, email)
    cursor.execute('''
        INSERT INTO clients(name, email) VALUES(?, ?)
    ''', data)
    connection.commit()


# Função para atualizar um registro na tabela clientes


def update(connection, cursor, name, email, id):
    data = (name, email, id)
    cursor.execute('''
        UPDATE clients SET name = ?, email = ? WHERE id = ?
    ''', data)
    connection.commit()


# Função para deletar um registro na tabela clientes


def delete(connection, cursor, id):
    data = (id,)
    cursor.execute('''
        DELETE FROM clients WHERE id = ?
    ''', data)
    connection.commit()

# Função para inserir vários registros na tabela clientes


def insert_many(connection, cursor, many_data):
    cursor.executemany('''
        INSERT INTO clients(name, email) VALUES(?, ?)
    ''', many_data)
    connection.commit()


# many_data = [
#     ("João", "john@gmail.com"),
#     ("Maria", "maria@example.com"),
#     ("Pedro", "pedro123@gmail.com"),
#     ("Ana", "ana.silva@yahoo.com"),
#     ("Carlos", "carlos.mota@hotmail.com"),
#     ("Fernanda", "fernanda123@outlook.com"),
#     ("Lucas", "lucas.tavares@gmail.com"),
#     ("Carla", "carla_oliveira@live.com"),
#     ("Rafael", "rafael1234@gmail.com"),
#     ("Patricia", "patricia.santos@icloud.com")
# ]
# insert_many(connection, cursor, many_data)
