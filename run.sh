#!/bin/bash
echo "🚀 Iniciando face_id_lojas..."

if [ ! -d "venv" ]; then
  echo "🔧 Criando ambiente virtual..."
  python3 -m venv venv
fi

source venv/bin/activate

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎬 Executando aplicação..."
python3 main.py