
import os
import cv2
import pickle
import numpy as np
import mss
from insightface.app import FaceAnalysis
from utils import CONFIG, get_monitor_region, cosine_similarity

SIM_THRESHOLD = 0.5

def carregar_embeddings():
    rostos = []
    base_path = "data"
    for pasta in os.listdir(base_path):
        pasta_path = os.path.join(base_path, pasta)
        emb_file = os.path.join(pasta_path, "embeddings.pkl")
        if os.path.isdir(pasta_path) and os.path.exists(emb_file):
            with open(emb_file, "rb") as f:
                dados = pickle.load(f)
                for nome, emb in dados:
                    rostos.append((nome, emb))
    return rostos

dados_face = carregar_embeddings()

region = get_monitor_region(CONFIG["monitor_entrada"]) if CONFIG["entrada"] == "monitor" else None
cap = mss.mss() if CONFIG["entrada"] == "monitor" else cv2.VideoCapture(CONFIG["camera_index"])

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))

while True:
    frame = np.array(cap.grab(region)) if CONFIG["entrada"] == "monitor" else cap.read()[1]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR) if CONFIG["entrada"] == "monitor" else frame

    faces = app.get(frame_rgb)

    for face in faces:
        melhor_sim = 0
        melhor_nome = None
        for nome, emb_salvo in dados_face:
            sim = cosine_similarity(face.embedding, emb_salvo)
            if sim > melhor_sim:
                melhor_sim = sim
                melhor_nome = nome

        if melhor_sim >= SIM_THRESHOLD:
            box = face.bbox.astype(int)
            nome_base = melhor_nome.split("|")[0]
            cv2.rectangle(frame_rgb, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            cv2.putText(frame_rgb, nome_base, (box[0], box[1]-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Reconhecimento Geral", frame_rgb)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
if CONFIG["entrada"] != "monitor":
    cap.release()
