@echo off
echo 🚀 Iniciando face_id_lojas...

IF NOT EXIST venv (
    echo 🔧 Criando ambiente virtual...
    python -m venv venv
)

call venv\Scripts\activate

echo 📦 Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

echo 🎬 Executando aplicação...
python main.py