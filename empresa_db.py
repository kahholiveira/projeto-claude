import sqlite3

# Criar o banco de dados empresa.db
conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()
print("Banco de dados empresa.db criado com sucesso!")

# Criar a tabela funcionarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario REAL NOT NULL
    )
''')
print("Tabela funcionarios criada com sucesso!")

# Inserir dois funcionários
cursor.execute('INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)', 
               ('Ana Costa', 'Gerente', 7000.00))
cursor.execute('INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)', 
               ('Carlos Lima', 'Programador', 5500.00))

conn.commit()
print("Dois funcionários inseridos com sucesso!")

# Imprimir os dados no terminal
cursor.execute('SELECT * FROM funcionarios')
funcionarios = cursor.fetchall()

print("\n=== DADOS DOS FUNCIONÁRIOS ===")
for funcionario in funcionarios:
    print(f"ID: {funcionario[0]}")
    print(f"Nome: {funcionario[1]}")
    print(f"Cargo: {funcionario[2]}")
    print(f"Salário: R$ {funcionario[3]:.2f}")
    print("-" * 30)

conn.close()
print("Conexão com banco de dados fechada.")