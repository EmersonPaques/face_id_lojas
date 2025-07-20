
import cv2
import os
import pickle
from insightface.app import FaceAnalysis
from utils import CONFIG, get_monitor_region
import mss
import numpy as np

app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

print("📌 Instruções: clique no rosto para selecionar.")

modo = input("Cadastrar em (loja/alerta)? ").strip().lower()
while modo not in ["loja", "alerta"]:
    modo = input("Digite 'loja' ou 'alerta': ").strip().lower()

if modo == "loja":
    nome_loja = input("Digite o nome da loja: ").strip().lower().replace(" ", "_")
    pasta_destino = os.path.join("data", nome_loja)
    os.makedirs(pasta_destino, exist_ok=True)
    motivo = ""
else:
    nome_loja = "alerta"
    pasta_destino = os.path.join("data", "alerta")
    os.makedirs(pasta_destino, exist_ok=True)
    motivo = input("Digite o motivo da inclusão: ").strip()

nome = input("Digite o nome da pessoa: ").strip().lower().replace(" ", "_")

region = get_monitor_region(CONFIG["monitor_entrada"]) if CONFIG["entrada"] == "monitor" else None
cap = mss.mss() if CONFIG["entrada"] == "monitor" else cv2.VideoCapture(CONFIG["camera_index"])

selecionadas = []

while True:
    frame = np.array(cap.grab(region)) if CONFIG["entrada"] == "monitor" else cap.read()[1]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR) if CONFIG["entrada"] == "monitor" else frame

    faces = app.get(frame_rgb)

    for face in faces:
        box = face.bbox.astype(int)
        cv2.rectangle(frame_rgb, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

    cv2.imshow("Cadastro - Clique em um rosto", frame_rgb)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break
    elif key == ord("s") and faces:
        print("Face selecionada para cadastro.")
        selecionadas.append(faces[0])
        break

cv2.destroyAllWindows()
if CONFIG["entrada"] != "monitor":
    cap.release()

if not selecionadas:
    print("Nenhuma face selecionada.")
    exit()

emb = selecionadas[0].embedding
arquivo_emb = os.path.join(pasta_destino, "embeddings.pkl")

if os.path.exists(arquivo_emb):
    with open(arquivo_emb, "rb") as f:
        dados = pickle.load(f)
else:
    dados = []

dados.append(((nome if not motivo else f"{nome}|{motivo}"), emb))

with open(arquivo_emb, "wb") as f:
    pickle.dump(dados, f)

print(f"✅ Pessoa '{nome}' cadastrada na loja '{nome_loja}'!")
