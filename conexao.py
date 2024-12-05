import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent
conexao = sqlite3.connect(ROOT_PATH/"meu-banco.db")
cursor = conexao.cursor()

# cursor.execute('''
#                CREATE TABLE clientes(
#                    id INTEGER PRIMARY KEY AUTOINCREMENT,
#                    nome VARCHAR(100),
#                    email VARCHAR(150)
#                 )
#                ''')

sql = "INSERT INTO clientes (id, nome, email) VALUES (?, ?, ?)"
dados = (1, "João Silva", "joao.silva@email.com")

cursor.execute(sql, dados)

conexao.commit()
