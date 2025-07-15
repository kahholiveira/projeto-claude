#!/usr/bin/env python3
"""
HR System - Sistema de Recursos Humanos
Flask web application with data visualization
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
import json
import sqlite3
import os
from datetime import datetime
from dateutil.parser import parse as parse_date

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
DATABASE = 'empresa.db'

def get_db_connection():
    """Conecta ao banco de dados SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa o banco de dados com dados de exemplo"""
    conn = get_db_connection()
    
    # Criar tabela se não existir
    conn.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cargo TEXT NOT NULL,
            salario REAL NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ativo BOOLEAN DEFAULT 1
        )
    ''')
    
    # Verificar se coluna ativo existe e adicionar se necessário
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(funcionarios)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'ativo' not in columns:
        conn.execute('ALTER TABLE funcionarios ADD COLUMN ativo BOOLEAN DEFAULT 1')
        print("📝 Coluna 'ativo' adicionada à tabela funcionarios")
    
    if 'data_cadastro' not in columns:
        conn.execute('ALTER TABLE funcionarios ADD COLUMN data_cadastro TIMESTAMP')
        # Atualizar registros existentes com data atual
        conn.execute("UPDATE funcionarios SET data_cadastro = datetime('now') WHERE data_cadastro IS NULL")
        print("📝 Coluna 'data_cadastro' adicionada à tabela funcionarios")
    
    # Verificar se já tem dados
    count = conn.execute('SELECT COUNT(*) FROM funcionarios').fetchone()[0]
    
    if count == 0:
        # Inserir dados de exemplo
        funcionarios_exemplo = [
            ('João Silva', 'Desenvolvedor', 5000.00),
            ('Maria Santos', 'Analista', 4500.00),
            ('Ana Costa', 'Gerente', 7000.00),
            ('Carlos Lima', 'Programador', 5500.00),
            ('Pedro Oliveira', 'Designer', 4000.00),
            ('Luciana Ferreira', 'Coordenadora', 6000.00),
            ('Roberto Almeida', 'Desenvolvedor Senior', 8000.00),
            ('Fernanda Rocha', 'Analista de Sistemas', 5200.00),
            ('Marcos Pereira', 'Tech Lead', 9000.00),
            ('Juliana Nascimento', 'Product Owner', 7500.00)
        ]
        
        for nome, cargo, salario in funcionarios_exemplo:
            conn.execute(
                'INSERT INTO funcionarios (nome, cargo, salario) VALUES (?, ?, ?)',
                (nome, cargo, salario)
            )
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    """Página principal"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HR System - Recursos Humanos</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .nav { margin: 20px 0; text-align: center; }
            .nav a { margin: 0 10px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; }
            .nav a:hover { background: #0056b3; }
            .stats { display: flex; justify-content: space-around; margin: 20px 0; }
            .stat-card { background: #f8f9fa; padding: 15px; border-radius: 4px; text-align: center; }
            .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 Sistema de Recursos Humanos</h1>
            
            <div class="nav">
                <a href="/funcionarios">👥 Funcionários</a>
                <a href="/dashboard">📊 Dashboard</a>
                <a href="/relatorios">📈 Relatórios</a>
                <a href="/api/funcionarios">🔗 API</a>
            </div>
            
            <div id="stats" class="stats">
                <div class="stat-card">
                    <div class="stat-number" id="total-funcionarios">-</div>
                    <div>Total Funcionários</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="salario-medio">-</div>
                    <div>Salário Médio</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number" id="total-cargos">-</div>
                    <div>Cargos Únicos</div>
                </div>
            </div>
            
            <script>
                fetch('/api/stats')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('total-funcionarios').textContent = data.total_funcionarios;
                        document.getElementById('salario-medio').textContent = 'R$ ' + data.salario_medio.toFixed(0);
                        document.getElementById('total-cargos').textContent = data.total_cargos;
                    });
            </script>
        </div>
    </body>
    </html>
    '''

@app.route('/funcionarios')
def funcionarios():
    """Lista todos os funcionários"""
    conn = get_db_connection()
    funcionarios = conn.execute(
        'SELECT * FROM funcionarios WHERE ativo = 1 ORDER BY nome'
    ).fetchall()
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Funcionários - HR System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; }
            .back-btn { background: #6c757d; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Voltar</a>
            <h1>👥 Funcionários Ativos</h1>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Cargo</th>
                        <th>Salário</th>
                        <th>Data Cadastro</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for funcionario in funcionarios:
        data_cadastro = funcionario['data_cadastro'] or 'N/A'
        html += f'''
                    <tr>
                        <td>{funcionario["id"]}</td>
                        <td>{funcionario["nome"]}</td>
                        <td>{funcionario["cargo"]}</td>
                        <td>R$ {funcionario["salario"]:,.2f}</td>
                        <td>{data_cadastro}</td>
                    </tr>
        '''
    
    html += '''
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''
    
    return html

@app.route('/dashboard')
def dashboard():
    """Dashboard com gráficos"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - HR System</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            .chart { margin: 20px 0; }
            .back-btn { background: #6c757d; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Voltar</a>
            <h1>📊 Dashboard</h1>
            
            <div class="chart">
                <h3>Distribuição de Salários por Cargo</h3>
                <div id="chart-salarios"></div>
            </div>
            
            <div class="chart">
                <h3>Quantidade de Funcionários por Cargo</h3>
                <div id="chart-cargos"></div>
            </div>
        </div>
        
        <script>
            // Carregar dados e criar gráficos
            fetch('/api/funcionarios')
                .then(response => response.json())
                .then(data => {
                    // Gráfico de salários
                    const salarios = {
                        x: data.map(f => f.cargo),
                        y: data.map(f => f.salario),
                        type: 'scatter',
                        mode: 'markers',
                        marker: { size: 12 },
                        name: 'Salários'
                    };
                    
                    Plotly.newPlot('chart-salarios', [salarios], {
                        title: 'Salários por Cargo',
                        xaxis: { title: 'Cargo' },
                        yaxis: { title: 'Salário (R$)' }
                    });
                    
                    // Gráfico de contagem por cargo
                    const cargos = {};
                    data.forEach(f => {
                        cargos[f.cargo] = (cargos[f.cargo] || 0) + 1;
                    });
                    
                    const cargoChart = {
                        values: Object.values(cargos),
                        labels: Object.keys(cargos),
                        type: 'pie'
                    };
                    
                    Plotly.newPlot('chart-cargos', [cargoChart], {
                        title: 'Distribuição por Cargo'
                    });
                });
        </script>
    </body>
    </html>
    '''

@app.route('/api/funcionarios')
def api_funcionarios():
    """API REST - Lista funcionários"""
    conn = get_db_connection()
    funcionarios = conn.execute(
        'SELECT * FROM funcionarios WHERE ativo = 1 ORDER BY nome'
    ).fetchall()
    conn.close()
    
    result = []
    for funcionario in funcionarios:
        result.append({
            'id': funcionario['id'],
            'nome': funcionario['nome'],
            'cargo': funcionario['cargo'],
            'salario': funcionario['salario'],
            'data_cadastro': funcionario['data_cadastro'],
            'ativo': funcionario['ativo']
        })
    
    return jsonify(result)

@app.route('/api/stats')
def api_stats():
    """API REST - Estatísticas"""
    conn = get_db_connection()
    
    # Total de funcionários ativos
    total = conn.execute(
        'SELECT COUNT(*) FROM funcionarios WHERE ativo = 1'
    ).fetchone()[0]
    
    # Salário médio
    salario_medio = conn.execute(
        'SELECT AVG(salario) FROM funcionarios WHERE ativo = 1'
    ).fetchone()[0] or 0
    
    # Total de cargos únicos
    total_cargos = conn.execute(
        'SELECT COUNT(DISTINCT cargo) FROM funcionarios WHERE ativo = 1'
    ).fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_funcionarios': total,
        'salario_medio': float(salario_medio),
        'total_cargos': total_cargos
    })

@app.route('/relatorios')
def relatorios():
    """Relatórios detalhados"""
    conn = get_db_connection()
    
    # Estatísticas por cargo
    stats_cargo = conn.execute('''
        SELECT 
            cargo,
            COUNT(*) as quantidade,
            AVG(salario) as salario_medio,
            MIN(salario) as salario_min,
            MAX(salario) as salario_max
        FROM funcionarios 
        WHERE ativo = 1 
        GROUP BY cargo 
        ORDER BY quantidade DESC
    ''').fetchall()
    
    conn.close()
    
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Relatórios - HR System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f8f9fa; }
            .back-btn { background: #6c757d; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        </style>
    </head>
    <body>
        <div class="container">
            <a href="/" class="back-btn">← Voltar</a>
            <h1>📈 Relatórios</h1>
            
            <h2>Estatísticas por Cargo</h2>
            <table>
                <thead>
                    <tr>
                        <th>Cargo</th>
                        <th>Quantidade</th>
                        <th>Salário Médio</th>
                        <th>Salário Mínimo</th>
                        <th>Salário Máximo</th>
                    </tr>
                </thead>
                <tbody>
    '''
    
    for stat in stats_cargo:
        html += f'''
                    <tr>
                        <td>{stat["cargo"]}</td>
                        <td>{stat["quantidade"]}</td>
                        <td>R$ {stat["salario_medio"]:,.2f}</td>
                        <td>R$ {stat["salario_min"]:,.2f}</td>
                        <td>R$ {stat["salario_max"]:,.2f}</td>
                    </tr>
        '''
    
    html += '''
                </tbody>
            </table>
        </div>
    </body>
    </html>
    '''
    
    return html

if __name__ == '__main__':
    import sys
    
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init':
            print("🔧 Inicializando banco de dados...")
            init_db()
            print("✅ Banco de dados inicializado com sucesso!")
            print("📊 Execute 'python3 hr_system.py' para iniciar o servidor")
            sys.exit(0)
        elif sys.argv[1] == 'reset':
            print("🗑️ Resetando banco de dados...")
            if os.path.exists(DATABASE):
                os.remove(DATABASE)
            init_db()
            print("✅ Banco de dados resetado com sucesso!")
            sys.exit(0)
        elif sys.argv[1] == 'test':
            print("🧪 Executando testes do sistema...")
            
            # Testar conexão com banco
            try:
                conn = get_db_connection()
                print("✅ Conexão com banco de dados: OK")
                
                # Testar contagem de funcionários
                count = conn.execute('SELECT COUNT(*) FROM funcionarios').fetchone()[0]
                print(f"✅ Total de funcionários no banco: {count}")
                
                # Testar dados básicos
                if count > 0:
                    funcionario = conn.execute('SELECT * FROM funcionarios LIMIT 1').fetchone()
                    print(f"✅ Primeiro funcionário: {funcionario['nome']} - {funcionario['cargo']}")
                
                # Testar estatísticas
                stats = conn.execute('''
                    SELECT 
                        COUNT(*) as total,
                        AVG(salario) as salario_medio,
                        COUNT(DISTINCT cargo) as total_cargos
                    FROM funcionarios WHERE ativo = 1
                ''').fetchone()
                
                print(f"✅ Estatísticas:")
                print(f"   - Total funcionários ativos: {stats['total']}")
                print(f"   - Salário médio: R$ {stats['salario_medio']:.2f}")
                print(f"   - Cargos únicos: {stats['total_cargos']}")
                
                conn.close()
                
                # Testar importações
                print("✅ Testando importações:")
                try:
                    import pandas as pd
                    print("   - pandas: OK")
                except ImportError:
                    print("   - pandas: ❌ ERRO")
                
                try:
                    import plotly.graph_objs as go
                    print("   - plotly: OK")
                except ImportError:
                    print("   - plotly: ❌ ERRO")
                
                try:
                    from flask import Flask
                    print("   - Flask: OK")
                except ImportError:
                    print("   - Flask: ❌ ERRO")
                
                try:
                    from flask_cors import CORS
                    print("   - Flask-CORS: OK")
                except ImportError:
                    print("   - Flask-CORS: ❌ ERRO")
                
                print("\n🎉 Todos os testes passaram!")
                print("Execute 'python3 hr_system.py' para iniciar o servidor")
                
            except Exception as e:
                print(f"❌ Erro durante o teste: {e}")
                sys.exit(1)
            
            sys.exit(0)
        elif sys.argv[1] == 'setup':
            print("🛠️ Configurando HR System...")
            
            # Verificar dependências
            print("\n📦 Verificando dependências:")
            missing_deps = []
            
            try:
                import flask
                print("   ✅ Flask instalado")
            except ImportError:
                print("   ❌ Flask não encontrado")
                missing_deps.append("Flask")
            
            try:
                import flask_cors
                print("   ✅ Flask-CORS instalado")
            except ImportError:
                print("   ❌ Flask-CORS não encontrado")
                missing_deps.append("Flask-CORS")
            
            try:
                import pandas
                print("   ✅ pandas instalado")
            except ImportError:
                print("   ❌ pandas não encontrado")
                missing_deps.append("pandas")
            
            try:
                import plotly
                print("   ✅ plotly instalado")
            except ImportError:
                print("   ❌ plotly não encontrado")
                missing_deps.append("plotly")
            
            try:
                import dateutil
                print("   ✅ python-dateutil instalado")
            except ImportError:
                print("   ❌ python-dateutil não encontrado")
                missing_deps.append("python-dateutil")
            
            if missing_deps:
                print(f"\n❌ Dependências faltando: {', '.join(missing_deps)}")
                print("Execute o comando:")
                print(f"pip install --break-system-packages {' '.join(missing_deps)}")
                sys.exit(1)
            
            print("\n✅ Todas as dependências estão instaladas!")
            
            # Configurar banco de dados
            print("\n🗄️ Configurando banco de dados...")
            try:
                init_db()
                print("✅ Banco de dados configurado com sucesso!")
            except Exception as e:
                print(f"❌ Erro ao configurar banco: {e}")
                sys.exit(1)
            
            # Verificar estrutura de arquivos
            print("\n📁 Verificando estrutura de arquivos:")
            files_to_check = [
                'hr_system.py',
                'requirements.txt',
                'empresa.db'
            ]
            
            for file in files_to_check:
                if os.path.exists(file):
                    print(f"   ✅ {file}")
                else:
                    print(f"   ❌ {file} não encontrado")
            
            # Mostrar informações do sistema
            print("\n🖥️ Informações do sistema:")
            print(f"   - Python: {sys.version.split()[0]}")
            print(f"   - Diretório atual: {os.getcwd()}")
            print(f"   - Banco de dados: {DATABASE}")
            
            # Testar servidor
            print("\n🌐 Testando configuração do servidor...")
            try:
                from flask import Flask
                test_app = Flask(__name__)
                print("   ✅ Flask pode criar aplicação")
            except Exception as e:
                print(f"   ❌ Erro ao testar Flask: {e}")
                sys.exit(1)
            
            print("\n🎉 Setup completo!")
            print("\nPróximos passos:")
            print("1. Execute 'python3 hr_system.py' para iniciar o servidor")
            print("2. Acesse http://localhost:5000 no navegador")
            print("3. Use 'python3 hr_system.py test' para verificar tudo")
            
            sys.exit(0)
        elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
            print("HR System - Sistema de Recursos Humanos")
            print("")
            print("Uso:")
            print("  python3 hr_system.py          # Iniciar servidor web")
            print("  python3 hr_system.py init     # Apenas inicializar banco")
            print("  python3 hr_system.py reset    # Resetar banco de dados")
            print("  python3 hr_system.py test     # Executar testes do sistema")
            print("  python3 hr_system.py setup    # Configuração completa do sistema")
            print("  python3 hr_system.py --help   # Mostrar esta ajuda")
            sys.exit(0)
        else:
            print(f"❌ Argumento desconhecido: {sys.argv[1]}")
            print("Use 'python3 hr_system.py --help' para ver opções disponíveis")
            sys.exit(1)
    
    # Inicializar banco de dados automaticamente
    init_db()
    
    print("🚀 Iniciando HR System...")
    print("📊 Dashboard disponível em: http://localhost:5000")
    print("👥 Funcionários em: http://localhost:5000/funcionarios")
    print("🔗 API em: http://localhost:5000/api/funcionarios")
    
    # Executar aplicação Flask
    app.run(debug=True, host='0.0.0.0', port=5000)