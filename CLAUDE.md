# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based employee management system that uses SQLite for data storage. The project consists of two main scripts that handle database operations for managing employee records in a company database.

## Architecture

### Core Components

- **cadastro.py**: Main script for employee registration that creates the database schema and inserts sample employee data
- **empresa_db.py**: Database initialization script with more detailed output formatting and employee insertion
- **empresa.db**: SQLite database file containing the `funcionarios` table

### Database Schema

The `funcionarios` table structure:
- `id`: INTEGER PRIMARY KEY AUTOINCREMENT
- `nome`: TEXT NOT NULL (employee name)
- `cargo`: TEXT NOT NULL (job position)
- `salario`: REAL NOT NULL (salary)

## Development Commands

### PostgreSQL Setup
```bash
# Option 1: Using Docker Compose (recommended)
docker-compose up -d
pip install -r requirements.txt

# Option 2: Using Docker directly
docker run --name postgres-empresa -e POSTGRES_PASSWORD=empresa123 -e POSTGRES_DB=empresa -p 5432:5432 -d postgres:15
pip install psycopg2-binary

# Option 3: Local PostgreSQL installation
sudo apt update && sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb empresa
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'empresa123';"
pip install psycopg2-binary
```

### Running the Application
```bash
# SQLite version (original)
python3 cadastro.py
python3 empresa_db.py

# PostgreSQL version (new)
python3 cadastro_postgres.py
```

### Database Operations
- **SQLite scripts**: Create local database file and insert sample data
- **PostgreSQL script**: Connects to PostgreSQL server, creates table with SERIAL primary key and DECIMAL salary field
- All scripts create the `funcionarios` table and insert sample employee records

## Project Structure

```
projeto_claude/
├── cadastro.py              # Original SQLite employee registration
├── empresa_db.py            # SQLite database setup with detailed logging
├── cadastro_postgres.py     # PostgreSQL version with proper error handling
├── docker-compose.yml       # PostgreSQL container configuration
├── requirements.txt         # Python dependencies (psycopg2-binary)
├── setup_postgres.sh        # Setup instructions script
├── empresa.db              # SQLite database (auto-generated)
└── CLAUDE.md               # This documentation
```

## Development Notes

### Database Options
- **SQLite**: Uses Python 3.12.3 built-in `sqlite3` module, no external dependencies
- **PostgreSQL**: Requires `psycopg2-binary` package and PostgreSQL server (Docker recommended)

### PostgreSQL Configuration
- Database: `empresa`
- User: `postgres`
- Password: `empresa123`
- Port: `5432`
- Table uses SERIAL for auto-increment and DECIMAL for precise salary storage

### Error Handling
- PostgreSQL script includes proper connection error handling
- Database connections are properly opened and closed in all scripts
- Scripts include sample data insertion for testing purposes