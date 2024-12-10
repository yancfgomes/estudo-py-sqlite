import sqlite3

from pathlib import Path


ROOT_PATH = Path(__file__).parent

# conexão
con = sqlite3.connect(ROOT_PATH/"desafio.db")

# cursor
cur = con.cursor()

# modo de retorno dos registros
cur.row_factory = sqlite3.Row


def create_table(con, cur):
    cur.execute('''
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100),
            email VARCHAR(150),
            tipo_cliente VARCHAR(20), -- 'Físico' ou 'Jurídico'
            cpf_cnpj VARCHAR(20) -- CPF ou CNPJ, dependendo do tipo de cliente
        );
    ''')
    con.commit()


# create_table(con, cur)


# Função para inserir dados de cliente
def inserir_cliente(cursor, conexao, nome, email, tipo_cliente, cpf_cnpj):
    try:
        if tipo_cliente not in ['Físico', 'Jurídico']:
            raise ValueError("Tipo de cliente inválido!")
        
        # Validação de CPF ou CNPJ
        if tipo_cliente == 'Físico' and len(cpf_cnpj) != 11:
            raise ValueError("CPF inválido!")
        elif tipo_cliente == 'Jurídico' and len(cpf_cnpj) != 14:
            raise ValueError("CNPJ inválido!")

        # Inserção no banco de dados
        cursor.execute("INSERT INTO clientes (nome, email, tipo_cliente, cpf_cnpj) VALUES (?, ?, ?, ?)", 
                       (nome, email, tipo_cliente, cpf_cnpj))
        conexao.commit()
        print("Cliente inserido com sucesso!")
    
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


# insert(con, cur, "Jessica", "jess@gmail.com", "Físico", "123.456.789-00")

data = [
    ('João da Silva', 'joão.da.silva@exemplo.com', 'Físico', '16290376418'),
    ('Ricardo Pereira', 'ricardo.pereira@exemplo.com', 'Físico', '40599023979'),
    ('Fernanda Santos', 'fernanda.santos@exemplo.com', 'Físico', '73899958176'),
    ('João da Silva', 'joão.da.silva@exemplo.com', 'Físico', '58241790942'),
    ('Consultoria Nova Era', 'consultoria.nova.era@exemplo.com', 'Jurídico', '98470525210407'),
    ('Soluções Inovadoras Ltda', 'soluções.inovadoras.ltda@exemplo.com', 'Jurídico', '50131394846374'),
    ('Fábrica Global', 'fábrica.global@exemplo.com', 'Jurídico', '15772040965575'),
    ('Escritório Jurídico Lopes', 'escritório.jurídico.lopes@exemplo.com', 'Jurídico', '70815673614480'),
    ('Indústria Alfa', 'indústria.alfa@exemplo.com', 'Jurídico', '51590533565574'),
    ('Tech Solutions Ltda', 'tech.solutions.ltda@exemplo.com', 'Jurídico', '67526754560534')
]


def insert_many(connection, cursor, many_data):
    cursor.executemany('''
        INSERT INTO clientes (nome, email, tipo_cliente, cpf_cnpj)
        VALUES(?, ?, ?, ?)
        ''', many_data)
    connection.commit()
    

# insert_many(con, cur, data)

def listar_clientes(cursor):
    return cursor.execute("SELECT * FROM clientes ORDER BY tipo_cliente;")


clientes = listar_clientes(cur)


for cliente in clientes:
    print(dict((cliente)))


