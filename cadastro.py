import sqlite3

conn = sqlite3.connect('empresa.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cargo TEXT NOT NULL,
        salario REAL NOT NULL
    )
''')

cursor.execute('INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)', 
               ('João Silva', 'Desenvolvedor', 5000.00))
cursor.execute('INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)', 
               ('Maria Santos', 'Analista', 4500.00))

conn.commit()

cursor.execute('SELECT * FROM funcionarios')
funcionarios = cursor.fetchall()

print("Funcionários cadastrados:")
for funcionario in funcionarios:
    print(f"ID: {funcionario[0]}, Nome: {funcionario[1]}, Cargo: {funcionario[2]}, Salário: R$ {funcionario[3]:.2f}")

conn.close()