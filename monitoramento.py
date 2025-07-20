
import os
import cv2
import pickle
import numpy as np
import mss
import winsound
import tkinter as tk
from tkinter import messagebox
from insightface.app import FaceAnalysis
from utils import CONFIG, get_monitor_region, cosine_similarity

SIM_THRESHOLD = 0.5

def carregar_embeddings():
    todas = []
    base_path = "data"
    for pasta in os.listdir(base_path):
        pasta_path = os.path.join(base_path, pasta)
        emb_file = os.path.join(pasta_path, "embeddings.pkl")
        if os.path.isdir(pasta_path) and os.path.exists(emb_file):
            with open(emb_file, "rb") as f:
                dados = pickle.load(f)
                for nome, emb in dados:
                    todas.append((nome, emb, pasta))
    return todas

def extrair_motivo(nome_completo):
    partes = nome_completo.split("|", 1)
    return partes[1] if len(partes) == 2 else None

dados_face = carregar_embeddings()

region = get_monitor_region(CONFIG["monitor_entrada"]) if CONFIG["entrada"] == "monitor" else None
cap = mss.mss() if CONFIG["entrada"] == "monitor" else cv2.VideoCapture(CONFIG["camera_index"])

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))

detectados = {}

def exibir_pop_up(nome, motivo):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("🚨 Alerta!", f"{nome} detectado!\nMotivo: {motivo}")
    root.destroy()

while True:
    frame = np.array(cap.grab(region)) if CONFIG["entrada"] == "monitor" else cap.read()[1]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR) if CONFIG["entrada"] == "monitor" else frame

    faces = app.get(frame_rgb)

    for face in faces:
        melhor_sim = 0
        melhor_nome = None
        melhor_pasta = None
        motivo = None

        for nome, emb_salvo, pasta in dados_face:
            sim = cosine_similarity(face.embedding, emb_salvo)
            if sim > melhor_sim:
                melhor_sim = sim
                melhor_nome = nome
                melhor_pasta = pasta

        if melhor_sim >= SIM_THRESHOLD:
            box = face.bbox.astype(int)
            nome_base = melhor_nome.split("|")[0]
            label = f"{nome_base} - {melhor_pasta}"
            cor = (255, 0, 0)  # azul padrão

            if melhor_pasta == "alerta":
                cor = (0, 0, 255)
                if nome_base not in detectados:
                    winsound.Beep(1200, 300)
                    motivo = extrair_motivo(melhor_nome)
                    exibir_pop_up(nome_base, motivo)
                    detectados[nome_base] = True
            else:
                detectados.pop(nome_base, None)

            cv2.rectangle(frame_rgb, (box[0], box[1]), (box[2], box[3]), cor, 2)
            cv2.putText(frame_rgb, label, (box[0], box[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

    cv2.imshow("Monitoramento Geral", frame_rgb)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
if CONFIG["entrada"] != "monitor":
    cap.release()
