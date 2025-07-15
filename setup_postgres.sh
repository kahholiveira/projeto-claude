#!/bin/bash

echo "Configurando PostgreSQL para o projeto..."

# Opção 1: Usando Docker Compose
echo "=== Opção 1: Docker Compose ==="
echo "Para usar Docker Compose:"
echo "1. docker-compose up -d"
echo "2. pip install -r requirements.txt"
echo "3. python3 cadastro_postgres.py"
echo ""

# Opção 2: Usando Docker diretamente
echo "=== Opção 2: Docker direto ==="
echo "Para usar Docker diretamente:"
echo "1. docker run --name postgres-empresa -e POSTGRES_PASSWORD=empresa123 -e POSTGRES_DB=empresa -p 5432:5432 -d postgres:15"
echo "2. pip install psycopg2-binary"
echo "3. python3 cadastro_postgres.py"
echo ""

# Opção 3: PostgreSQL local
echo "=== Opção 3: PostgreSQL local ==="
echo "Para instalar PostgreSQL localmente:"
echo "1. sudo apt update && sudo apt install postgresql postgresql-contrib"
echo "2. sudo -u postgres createdb empresa"
echo "3. sudo -u postgres psql -c \"ALTER USER postgres PASSWORD 'empresa123';\""
echo "4. pip install psycopg2-binary"
echo "5. python3 cadastro_postgres.py"