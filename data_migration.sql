-- Migração de dados para o sistema de funcionários
-- Este script insere dados iniciais na tabela funcionarios

-- Inserir funcionários de exemplo
INSERT INTO funcionarios (nome, cargo, salario) VALUES 
('João Silva', 'Desenvolvedor', 5000.00),
('Maria Santos', 'Analista', 4500.00),
('Ana Costa', 'Gerente', 7000.00),
('Carlos Lima', 'Programador', 5500.00),
('Pedro Oliveira', 'Designer', 4000.00),
('Luciana Ferreira', 'Coordenadora', 6000.00),
('Roberto Almeida', 'Desenvolvedor Senior', 8000.00),
('Fernanda Rocha', 'Analista de Sistemas', 5200.00),
('Marcos Pereira', 'Tech Lead', 9000.00),
('Juliana Nascimento', 'Product Owner', 7500.00);

-- Inserir alguns funcionários inativos para teste
INSERT INTO funcionarios (nome, cargo, salario, ativo) VALUES 
('José Santos', 'Ex-funcionário', 4500.00, false),
('Maria Aparecida', 'Ex-analista', 4000.00, false);

-- Verificar os dados inseridos
SELECT 
    id,
    nome,
    cargo,
    salario,
    data_cadastro,
    ativo
FROM funcionarios 
ORDER BY id;

-- Estatísticas dos dados inseridos
SELECT 
    COUNT(*) as total_funcionarios,
    COUNT(*) FILTER (WHERE ativo = true) as funcionarios_ativos,
    COUNT(*) FILTER (WHERE ativo = false) as funcionarios_inativos,
    AVG(salario) as salario_medio,
    MIN(salario) as menor_salario,
    MAX(salario) as maior_salario
FROM funcionarios;