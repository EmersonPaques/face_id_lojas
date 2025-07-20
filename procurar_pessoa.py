
import os
import cv2
import pickle
import mss
import numpy as np
from insightface.app import FaceAnalysis
from utils import CONFIG, get_monitor_region, cosine_similarity
import pytesseract
import winsound
import tkinter as tk
from tkinter import scrolledtext

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

SIM_THRESHOLD = 0.5

def listar_pastas():
    return [p for p in os.listdir("data") if os.path.isdir(os.path.join("data", p))]

def listar_pessoas(pasta):
    emb_file = os.path.join("data", pasta, "embeddings.pkl")
    if not os.path.exists(emb_file):
        return []
    with open(emb_file, "rb") as f:
        dados = pickle.load(f)
    return [d[0] for d in dados]

print("Escolha a pasta (loja ou alerta):")
pastas = listar_pastas()
for i, pasta in enumerate(pastas):
    print(f"{i+1}. {pasta}")
idx_pasta = int(input("Número da pasta: ")) - 1
pasta_escolhida = pastas[idx_pasta]

pessoas = listar_pessoas(pasta_escolhida)
if not pessoas:
    print("Nenhum cadastro encontrado.")
    exit()

print("\nPessoas encontradas:")
for i, p in enumerate(pessoas):
    if "|" in p:
        nome, motivo = p.split("|", 1)
        print(f"{i+1}. {nome} ({motivo})")
    else:
        print(f"{i+1}. {p}")
idx_pessoa = int(input("Número da pessoa: ")) - 1
pessoa_alvo = pessoas[idx_pessoa]

print(f"🔍 Procurando por {pessoa_alvo}")

# Carrega embeddings da pessoa
emb_file = os.path.join("data", pasta_escolhida, "embeddings.pkl")
with open(emb_file, "rb") as f:
    dados = pickle.load(f)

alvo_embeddings = [emb for nome, emb in dados if nome == pessoa_alvo]

# Setup OCR + janela de horários
root = tk.Tk()
root.title("Horários detectados")
text_box = scrolledtext.ScrolledText(root, width=40, height=10)
text_box.pack()
text_box.insert(tk.END, "⏱️ Horários encontrados:\n")

def adicionar_horario(text):
    text_box.insert(tk.END, f"{text}\n")
    text_box.see(tk.END)

region = get_monitor_region(CONFIG["monitor_entrada"]) if CONFIG["entrada"] == "monitor" else None
cap = mss.mss() if CONFIG["entrada"] == "monitor" else cv2.VideoCapture(CONFIG["camera_index"])

ja_alertado = False

def extrair_hora(frame):
    roi = frame[0:60, -300:]  # canto superior direito
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip().replace("\n", " ")

face_app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
face_app.prepare(ctx_id=0, det_size=(640, 640))

while True:
    frame = np.array(cap.grab(region)) if CONFIG["entrada"] == "monitor" else cap.read()[1]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR) if CONFIG["entrada"] == "monitor" else frame
    faces = face_app.get(frame_rgb)

    detectado = False

    for face in faces:
        sim = max([cosine_similarity(face.embedding, emb) for emb in alvo_embeddings])
        if sim >= SIM_THRESHOLD:
            box = face.bbox.astype(int)
            cv2.rectangle(frame_rgb, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
            cv2.putText(frame_rgb, f"{pessoa_alvo}", (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

            if not ja_alertado:
                winsound.Beep(1000, 300)
                horario = extrair_hora(frame_rgb)
                adicionar_horario(horario)
                ja_alertado = True
            detectado = True
            break

    if not detectado:
        ja_alertado = False

    cv2.imshow("Procurar Pessoa", frame_rgb)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    root.update()

cv2.destroyAllWindows()
root.destroy()
if CONFIG["entrada"] != "monitor":
    cap.release()
