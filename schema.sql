-- Schema para o sistema de cadastro de funcionários
-- PostgreSQL Database Schema

-- Criar banco de dados (se executado via psql como superuser)
-- CREATE DATABASE empresa;

-- Conectar ao banco empresa
-- \c empresa;

-- Remover tabela se existir (para recriar)
DROP TABLE IF EXISTS funcionarios;

-- Criar tabela funcionarios
CREATE TABLE funcionarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT true
);

-- Criar índices para melhor performance
CREATE INDEX idx_funcionarios_nome ON funcionarios(nome);
CREATE INDEX idx_funcionarios_cargo ON funcionarios(cargo);
CREATE INDEX idx_funcionarios_ativo ON funcionarios(ativo);

-- Comentários nas colunas
COMMENT ON TABLE funcionarios IS 'Tabela de funcionários da empresa';
COMMENT ON COLUMN funcionarios.id IS 'Identificador único do funcionário';
COMMENT ON COLUMN funcionarios.nome IS 'Nome completo do funcionário';
COMMENT ON COLUMN funcionarios.cargo IS 'Cargo/função do funcionário';
COMMENT ON COLUMN funcionarios.salario IS 'Salário do funcionário em reais';
COMMENT ON COLUMN funcionarios.data_cadastro IS 'Data e hora do cadastro';
COMMENT ON COLUMN funcionarios.ativo IS 'Status ativo/inativo do funcionário';