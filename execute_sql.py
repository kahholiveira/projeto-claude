#!/usr/bin/env python3
"""
Script para executar schema.sql e data_migration.sql
"""
import psycopg2
import sys
import os

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'database': 'empresa',
    'user': 'postgres',
    'password': 'empresa123',
    'port': '5432'
}

def execute_sql_file(cursor, filename):
    """Executa um arquivo SQL"""
    if not os.path.exists(filename):
        print(f"Erro: Arquivo {filename} não encontrado!")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Separar comandos por ';' e executar cada um
        commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
        
        for i, command in enumerate(commands):
            if command.startswith('--') or not command:
                continue
            try:
                cursor.execute(command)
                print(f"✓ Comando {i+1} de {filename} executado com sucesso")
            except Exception as e:
                print(f"✗ Erro no comando {i+1} de {filename}: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"Erro ao ler arquivo {filename}: {e}")
        return False

def main():
    """Função principal"""
    try:
        # Conectar ao PostgreSQL
        print("Conectando ao PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True  # Para comandos DDL
        cursor = conn.cursor()
        print("✓ Conectado com sucesso!")
        
        # Executar schema.sql primeiro
        print("\n1. Executando schema.sql...")
        if execute_sql_file(cursor, 'schema.sql'):
            print("✓ schema.sql executado com sucesso!")
        else:
            print("✗ Falha ao executar schema.sql")
            return 1
        
        # Executar data_migration.sql depois
        print("\n2. Executando data_migration.sql...")
        if execute_sql_file(cursor, 'data_migration.sql'):
            print("✓ data_migration.sql executado com sucesso!")
        else:
            print("✗ Falha ao executar data_migration.sql")
            return 1
        
        # Verificar resultado
        print("\n3. Verificando resultado...")
        cursor.execute("SELECT COUNT(*) FROM funcionarios")
        count = cursor.fetchone()[0]
        print(f"✓ Total de funcionários cadastrados: {count}")
        
        cursor.execute("SELECT nome, cargo, salario FROM funcionarios LIMIT 5")
        funcionarios = cursor.fetchall()
        print("\nPrimeiros 5 funcionários:")
        for func in funcionarios:
            print(f"  - {func[0]}, {func[1]}, R$ {func[2]:.2f}")
        
    except psycopg2.Error as e:
        print(f"Erro PostgreSQL: {e}")
        print("\nVerifique se:")
        print("1. PostgreSQL está rodando (docker run --name postgres-empresa -e POSTGRES_PASSWORD=empresa123 -e POSTGRES_DB=empresa -p 5432:5432 -d postgres:15)")
        print("2. As credenciais estão corretas")
        print("3. O banco 'empresa' existe")
        return 1
    except Exception as e:
        print(f"Erro geral: {e}")
        return 1
    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()
            print("\n✓ Conexão fechada.")
    
    print("\n🎉 Migração concluída com sucesso!")
    return 0

if __name__ == "__main__":
    sys.exit(main())