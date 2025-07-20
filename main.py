
import os
import json
from utils import selecionar_entrada, selecionar_monitor

CONFIG_FILE = "config.json"

def salvar_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def carregar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def menu():
    print("\n===== Reconhecimento Facial por Loja =====")
    print("1. Cadastrar nova pessoa")
    print("2. Iniciar reconhecimento")
    print("3. Procurar pessoa salva")
    print("4. Monitoramento (todas as pastas)")
    print("5. Alterar pessoa cadastrada")
    print("6. Sair")
    return input("Escolha uma opção: ")

# Carrega ou define entrada
config = carregar_config()
if not config:
    entrada, camera_index = selecionar_entrada()
    monitor_id = selecionar_monitor()
    config = {
        "entrada": entrada,
        "camera_index": camera_index,
        "monitor_entrada": monitor_id
    }
    salvar_config(config)

# Atualiza config global em utils
import utils
utils.CONFIG = config

while True:
    opcao = menu()
    if opcao == "1":
        os.system("python cadastro.py")
    elif opcao == "2":
        os.system("python reconhecimento.py")
    elif opcao == "3":
        os.system("python procurar_pessoa.py")
    elif opcao == "4":
        os.system("python monitoramento.py")
    elif opcao == "5":
        os.system("python alterar_cadastro.py")
    elif opcao == "6":
        print("Encerrando.")
        break
    else:
        print("Opção inválida.")
