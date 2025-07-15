#!/bin/bash

echo "=== Instalando Dependências do Projeto ==="

# Verificar se pip está instalado
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip não encontrado. Instalando pip..."
    
    # Baixar get-pip.py
    if command -v curl &> /dev/null; then
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    elif command -v wget &> /dev/null; then
        wget https://bootstrap.pypa.io/get-pip.py
    else
        echo "❌ curl ou wget necessário para baixar pip"
        echo "Instale manualmente:"
        echo "  sudo apt update"
        echo "  sudo apt install python3-pip"
        exit 1
    fi
    
    # Instalar pip
    python3 get-pip.py --user
    
    # Adicionar ao PATH se necessário
    export PATH="$HOME/.local/bin:$PATH"
    
    # Limpar arquivo temporário
    rm -f get-pip.py
    
    echo "✅ pip instalado com sucesso!"
fi

# Verificar se pip funciona agora
if command -v pip &> /dev/null; then
    PIP_CMD="pip"
elif command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif python3 -m pip --version &> /dev/null; then
    PIP_CMD="python3 -m pip"
else
    echo "❌ Não foi possível encontrar pip funcionando"
    echo "Tente instalar manualmente:"
    echo "  sudo apt update"
    echo "  sudo apt install python3-pip"
    exit 1
fi

echo "✅ Usando: $PIP_CMD"

# Instalar dependências
echo "Instalando psycopg2-binary..."
$PIP_CMD install --user psycopg2-binary==2.9.9

echo ""
echo "✅ Dependências instaladas com sucesso!"
echo ""
echo "Agora você pode executar:"
echo "  python3 execute_sql.py"
echo "  python3 cadastro_postgres.py"