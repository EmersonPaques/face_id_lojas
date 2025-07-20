
import os
import cv2
import pickle
import tkinter as tk
from tkinter import filedialog
from insightface.app import FaceAnalysis
import numpy as np

print("=== Cadastro manual por imagens ===")
nome = input("Nome da pessoa: ").strip()
tipo = input("Destino (loja/alerta): ").strip().lower()

if tipo == "alerta":
    motivo = input("Motivo da inclusão: ").strip()
    nome += "|" + motivo
    pasta = "alerta"
else:
    pasta = tipo

destino = os.path.join("data", pasta)
os.makedirs(destino, exist_ok=True)

root = tk.Tk()
root.withdraw()
arquivos = filedialog.askopenfilenames(
    title="Selecione imagens da pessoa",
    filetypes=[("Imagens", "*.jpg *.jpeg *.png")]
)
if not arquivos:
    print("Nenhuma imagem selecionada.")
    exit()

print(f"Selecionadas {len(arquivos)} imagens.")

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))

embeddings = []
for img_path in arquivos:
    img = cv2.imread(img_path)
    faces = app.get(img)
    if faces:
        emb = faces[0].embedding
        embeddings.append((nome, emb))
        print(f"✅ Embedding extraído de {os.path.basename(img_path)}")
    else:
        print(f"⚠️ Nenhum rosto detectado em {os.path.basename(img_path)}")

# Salvar embeddings
emb_file = os.path.join(destino, "embeddings.pkl")
if os.path.exists(emb_file):
    with open(emb_file, "rb") as f:
        existentes = pickle.load(f)
else:
    existentes = []

existentes.extend(embeddings)
with open(emb_file, "wb") as f:
    pickle.dump(existentes, f)

print(f"✅ {len(embeddings)} embeddings salvos para '{nome}' em {pasta}")
