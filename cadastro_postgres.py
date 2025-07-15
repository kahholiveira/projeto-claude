import psycopg2
from psycopg2 import sql

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'database': 'empresa',
    'user': 'postgres',
    'password': 'empresa123',
    'port': '5432'
}

try:
    # Conectar ao PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Criar tabela funcionarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cargo VARCHAR(50) NOT NULL,
            salario DECIMAL(10,2) NOT NULL
        )
    ''')
    
    # Inserir funcionários de exemplo
    cursor.execute('''
        INSERT INTO funcionarios (nome, cargo, salario) 
        VALUES (%s, %s, %s)
    ''', ('João Silva', 'Desenvolvedor', 5000.00))
    
    cursor.execute('''
        INSERT INTO funcionarios (nome, cargo, salario) 
        VALUES (%s, %s, %s)
    ''', ('Maria Santos', 'Analista', 4500.00))
    
    conn.commit()
    
    # Consultar todos os funcionários
    cursor.execute('SELECT * FROM funcionarios')
    funcionarios = cursor.fetchall()
    
    print("Funcionários cadastrados:")
    for funcionario in funcionarios:
        print(f"ID: {funcionario[0]}, Nome: {funcionario[1]}, Cargo: {funcionario[2]}, Salário: R$ {funcionario[3]:.2f}")
    
except psycopg2.Error as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")
    
finally:
    if 'conn' in locals():
        cursor.close()
        conn.close()
        print("Conexão com PostgreSQL fechada.")