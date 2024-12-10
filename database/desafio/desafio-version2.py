import sqlite3
from pathlib import Path


# Configuração do banco de dados
ROOT_PATH = Path(__file__).parent
DB_PATH = ROOT_PATH / "desafio-v2.db"


def create_connection(db_path):
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def create_table(cursor):
    """Cria a tabela 'clientes' no banco de dados."""
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100),
                email VARCHAR(150),
                tipo_cliente VARCHAR(20), -- 'Físico' ou 'Jurídico'
                cpf_cnpj VARCHAR(20) -- CPF ou CNPJ, dependendo do tipo de
                cliente
            );
        ''')
        print("Tabela criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")


def validate_client_data(tipo_cliente, cpf_cnpj):
    """Valida os dados de cliente antes de inseri-los no banco."""
    if tipo_cliente not in ['Físico', 'Jurídico']:
        raise ValueError("Tipo de cliente inválido!")

    if tipo_cliente == 'Físico' and len(cpf_cnpj) != 11:
        raise ValueError("CPF inválido!")

    if tipo_cliente == 'Jurídico' and len(cpf_cnpj) != 14:
        raise ValueError("CNPJ inválido!")


def insert_client(cursor, nome, email, tipo_cliente, cpf_cnpj):
    """Insere um cliente no banco de dados."""
    try:
        validate_client_data(tipo_cliente, cpf_cnpj)
        
        cursor.execute("""
            INSERT INTO clientes (nome, email, tipo_cliente, cpf_cnpj)
            VALUES (?, ?, ?, ?)
        """, (nome, email, tipo_cliente, cpf_cnpj))
        
        print(f"Cliente {nome} inserido com sucesso!")
    except ValueError as ve:
        print(f"Erro de validação: {ve}")
    except sqlite3.Error as e:
        print(f"Erro ao inserir dados no banco de dados: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def insert_multiple_clients(cursor, many_data):
    """Insere múltiplos clientes de uma vez no banco de dados."""
    try:
        cursor.executemany("""
            INSERT INTO clientes (nome, email, tipo_cliente, cpf_cnpj)
            VALUES (?, ?, ?, ?)
        """, many_data)
        print("Clientes inseridos com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir múltiplos clientes: {e}")


def list_clients(cursor):
    """Lista todos os clientes do banco de dados."""
    try:
        cursor.execute("SELECT * FROM clientes ORDER BY tipo_cliente")
        clients = cursor.fetchall()

        if not clients:
            print("Nenhum cliente encontrado.")
            return

        for client in clients:
            tipo = 'Pessoa Física' if client['tipo_cliente'] == 'Físico' else 'Pessoa Jurídica'
            print(f"ID: {client['id']}, Nome: {client['nome']}, Tipo: {tipo}, CPF/CNPJ: {client['cpf_cnpj']}")

    except sqlite3.Error as e:
        print(f"Erro ao listar os clientes: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def main():
    """Função principal que controla o fluxo do programa."""
    # Criar conexão
    connection = create_connection(DB_PATH)
    if connection is None:
        return
    
    cursor = connection.cursor()

    # Criar tabela
    create_table(cursor)

    # Inserir um cliente de exemplo
    insert_client(cursor, "Jessica", "jess@gmail.com", "Físico", "12345678900")

    # Inserir múltiplos clientes
    multiple_data = [
        ('João da Silva', 'joão.da.silva@exemplo.com', 'Físico', '16290376418'),
        ('Ricardo Pereira', 'ricardo.pereira@exemplo.com', 'Físico', '40599023979'),
        ('Fernanda Santos', 'fernanda.santos@exemplo.com', 'Físico', '73899958176'),
        ('Consultoria Nova Era', 'consultoria.nova.era@exemplo.com', 'Jurídico', '98470525210407'),
        ('Soluções Inovadoras Ltda', 'soluções.inovadoras.ltda@exemplo.com', 'Jurídico', '50131394846374')
    ]
    insert_multiple_clients(cursor, multiple_data)

    # Listar clientes
    list_clients(cursor)

    # Fechar conexão
    connection.close()


if __name__ == "__main__":
    main()
