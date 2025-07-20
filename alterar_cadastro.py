
import os
import pickle

def listar_pastas():
    return [p for p in os.listdir("data") if os.path.isdir(os.path.join("data", p))]

def listar_pessoas(pasta):
    emb_file = os.path.join("data", pasta, "embeddings.pkl")
    if not os.path.exists(emb_file):
        return []
    with open(emb_file, "rb") as f:
        return pickle.load(f)

def salvar_pessoas(pasta, dados):
    emb_file = os.path.join("data", pasta, "embeddings.pkl")
    with open(emb_file, "wb") as f:
        pickle.dump(dados, f)

print("=== Alterar pessoa cadastrada ===")
pastas = listar_pastas()
for i, pasta in enumerate(pastas):
    print(f"{i+1}. {pasta}")
idx = int(input("Escolha uma pasta: ")) - 1
pasta = pastas[idx]

pessoas = listar_pessoas(pasta)
if not pessoas:
    print("Nenhuma pessoa encontrada.")
    exit()

print("\nPessoas:")
for i, (nome, _) in enumerate(pessoas):
    if "|" in nome:
        nome_exib, motivo = nome.split("|", 1)
        print(f"{i+1}. {nome_exib} ({motivo})")
    else:
        print(f"{i+1}. {nome}")
idx_pessoa = int(input("Escolha a pessoa para alterar: ")) - 1

nome_antigo, emb = pessoas[idx_pessoa]
nome_base = nome_antigo.split("|")[0]
motivo_antigo = nome_antigo.split("|")[1] if "|" in nome_antigo else ""

novo_nome = input(f"Novo nome [{nome_base}]: ").strip()
if pasta == "alerta":
    novo_motivo = input(f"Novo motivo [{motivo_antigo}]: ").strip()
else:
    novo_motivo = ""

final_nome = (novo_nome if novo_nome else nome_base)
if pasta == "alerta":
    final_nome += "|" + (novo_motivo if novo_motivo else motivo_antigo)

pessoas[idx_pessoa] = (final_nome, emb)
salvar_pessoas(pasta, pessoas)

print("✅ Cadastro atualizado com sucesso.")
