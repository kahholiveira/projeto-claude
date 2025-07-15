#!/bin/bash

echo "=== Executando Schema e Migração de Dados ==="

# Verificar se PostgreSQL está rodando
echo "1. Verificando se PostgreSQL está rodando..."
if ! command -v psql &> /dev/null; then
    echo "❌ psql não encontrado. Tentando via Docker..."
    
    # Verificar se container já existe
    if docker ps -a --format "table {{.Names}}" | grep -q "postgres-empresa"; then
        echo "Container postgres-empresa já existe. Iniciando..."
        docker start postgres-empresa 2>/dev/null || echo "Container já rodando"
    else
        echo "Criando container PostgreSQL..."
        docker run --name postgres-empresa \
            -e POSTGRES_PASSWORD=empresa123 \
            -e POSTGRES_DB=empresa \
            -p 5432:5432 \
            -d postgres:15
    fi
    
    # Aguardar PostgreSQL inicializar
    echo "Aguardando PostgreSQL inicializar..."
    sleep 10
    
    # Executar SQLs via Docker
    echo "2. Executando schema.sql..."
    docker exec -i postgres-empresa psql -U postgres -d empresa < schema.sql
    
    echo "3. Executando data_migration.sql..."
    docker exec -i postgres-empresa psql -U postgres -d empresa < data_migration.sql
    
    echo "4. Verificando dados..."
    docker exec -i postgres-empresa psql -U postgres -d empresa -c "SELECT COUNT(*) as total_funcionarios FROM funcionarios;"
    
else
    # Usar psql local
    echo "✅ psql encontrado. Usando PostgreSQL local..."
    
    export PGPASSWORD=empresa123
    
    echo "2. Executando schema.sql..."
    psql -h localhost -U postgres -d empresa -f schema.sql
    
    echo "3. Executando data_migration.sql..."
    psql -h localhost -U postgres -d empresa -f data_migration.sql
    
    echo "4. Verificando dados..."
    psql -h localhost -U postgres -d empresa -c "SELECT COUNT(*) as total_funcionarios FROM funcionarios;"
fi

echo "🎉 Migração concluída!"
echo ""
echo "Para conectar ao banco:"
echo "docker exec -it postgres-empresa psql -U postgres -d empresa"
echo "ou"
echo "psql -h localhost -U postgres -d empresa"