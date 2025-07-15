# Setup Completo do Projeto

## ✅ Status Atual
- ✅ Dependências instaladas: `psycopg2-binary`
- ✅ Scripts SQL criados: `schema.sql`, `data_migration.sql`
- ✅ Scripts de execução prontos
- ❌ PostgreSQL não está rodando (necessário para executar)

## 🐳 Para executar com Docker (recomendado)

### 1. Configurar permissões Docker (uma vez apenas)
```bash
# Adicionar usuário ao grupo docker
sudo usermod -a -G docker $USER

# Reiniciar sessão ou executar:
newgrp docker

# Ou executar comandos docker com sudo
```

### 2. Iniciar PostgreSQL
```bash
# Iniciar container PostgreSQL
docker run --name postgres-empresa \
  -e POSTGRES_PASSWORD=empresa123 \
  -e POSTGRES_DB=empresa \
  -p 5432:5432 \
  -d postgres:15

# Aguardar alguns segundos para inicializar
sleep 10
```

### 3. Executar migração
```bash
# Executar schema.sql e data_migration.sql
python3 execute_sql.py

# Ou usar o script bash
./run_migration.sh
```

## 🔧 Para executar com PostgreSQL local

### 1. Instalar PostgreSQL
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Configurar banco
```bash
sudo -u postgres createdb empresa
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'empresa123';"
```

### 3. Executar migração
```bash
export PGPASSWORD=empresa123
psql -h localhost -U postgres -d empresa -f schema.sql
psql -h localhost -U postgres -d empresa -f data_migration.sql
```

## 📁 Arquivos do Projeto

### Scripts SQL
- **`schema.sql`**: Cria tabela `funcionarios` com índices e comentários
- **`data_migration.sql`**: Insere 12 funcionários de exemplo

### Scripts Python
- **`execute_sql.py`**: Executa os SQLs via Python (requer PostgreSQL rodando)
- **`cadastro_postgres.py`**: Script principal para PostgreSQL
- **`cadastro.py`**: Script original SQLite

### Scripts de Setup
- **`run_migration.sh`**: Executa migração via Docker ou psql
- **`install_dependencies.sh`**: Instala dependências Python

## 🚀 Comandos Prontos

```bash
# 1. Iniciar PostgreSQL (com permissões Docker)
docker run --name postgres-empresa -e POSTGRES_PASSWORD=empresa123 -e POSTGRES_DB=empresa -p 5432:5432 -d postgres:15

# 2. Executar migração
python3 execute_sql.py

# 3. Testar aplicação
python3 cadastro_postgres.py

# 4. Conectar ao banco
docker exec -it postgres-empresa psql -U postgres -d empresa
```

## ✅ Resultado Esperado
- Tabela `funcionarios` criada com 12 registros
- 10 funcionários ativos, 2 inativos
- Índices e constraints aplicados
- Campos: id, nome, cargo, salario, data_cadastro, ativo