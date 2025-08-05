import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
import os, pickle, time
import cv2
import mss
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime, date
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity
from pytesseract import image_to_string
from screeninfo import get_monitors

# --- Inicialização InsightFace ---
face_app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=0, det_size=(640, 640))

# --- Helpers Embeddings e OCR ---
def load_all_embeddings():
    rostos = []
    for pasta in os.listdir("data"):
        fpath = os.path.join("data", pasta, "embeddings.pkl")
        if os.path.isdir(os.path.join("data", pasta)) and os.path.exists(fpath):
            rostos += [(nome, emb, pasta) for nome, emb in pickle.load(open(fpath,'rb'))]
    return rostos

def load_target_embeddings(pasta, pessoa):
    fpath = f"data/{pasta}/embeddings.pkl"
    if not os.path.exists(fpath):
        return []
    return [emb for nome, emb in pickle.load(open(fpath,'rb')) if nome.split("|")[0] == pessoa]

def save_embedding(nome, emb):
    app.lift()
    pasta = simpledialog.askstring("Loja/Alerta", "Digite loja ou 'alerta':", parent=app)
    if not pasta:
        return
    os.makedirs(f"data/{pasta}", exist_ok=True)
    fpath = f"data/{pasta}/embeddings.pkl"
    dados = pickle.load(open(fpath,'rb')) if os.path.exists(fpath) else []
    dados.append((nome, emb))
    pickle.dump(dados, open(fpath,'wb'))
    app.lift()
    messagebox.showinfo("Salvo", f"Embedding de '{nome}' salvo em '{pasta}'", parent=app)

# --- Configurações de DETECÇÃO ---
DETECTIONS_FOLDER = "detecções"

monitores = get_monitors()
monitor_exib = 0
monitor_analise = 1 if len(monitores) > 1 else 0

def swap_monitors():
    global monitor_exib, monitor_analise
    monitor_exib, monitor_analise = monitor_analise, monitor_exib
    m = monitores[monitor_exib]
    app.geometry(f"{m.width}x{m.height}+{m.x}+{m.y}")

# --- App Principal ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.mode = "general"
        self.search_pasta = self.search_nome = None
        self.detected_faces = []
        self.notified_today = set()
        self.current_date = date.today().isoformat()
        os.makedirs("data", exist_ok=True)
        os.makedirs(DETECTIONS_FOLDER, exist_ok=True)

        # Posiciona na tela de exibição
        m = monitores[monitor_exib]
        self.geometry(f"{m.width}x{m.height}+{m.x}+{m.y}")
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.config(bg='black')

        self._build_ui()

        # Prepara captura e item de imagem
        self.sct = mss.mss()
        self.photo = None
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor='nw', image=None)

        # Inicia loop via after
        self.after(0, self.update_frame)

    def _build_ui(self):
        btns = tk.Frame(self, bg='#222')
        btns.pack(fill=tk.X)
        for txt, cmd in [
            ("🔄 Swap Telas", swap_monitors),
            ("🔄 Geral",     lambda: self._set_mode("general")),
            ("🔍 Buscar",    self._choose_person),
            ("📡 Monitor",   lambda: self._set_mode("monitor")),
            ("➕ Cadastrar", lambda: self._set_mode("register")),
            ("📷 Webcam",    self._webcam_register),
            ("✖︎ Sair",      self.quit),
        ]:
            tk.Button(btns, text=txt, command=cmd).pack(side=tk.LEFT, padx=3, pady=3)
        self.canvas = tk.Canvas(self, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self._on_click)

    def _set_mode(self, m):
        self.mode = m
        self.notified_today.clear()
        self.lift()
        titles = {
            "general": "Modo Geral",
            "monitor": "Monitoramento",
            "search":  "Buscar Pessoa",
            "register":"Clique para cadastrar"
        }
        messagebox.showinfo("Modo", titles.get(m, ""), parent=self)

    def _choose_person(self):
        self.lift()
        pasta = simpledialog.askstring("Pasta", "Digite loja ou alerta:", parent=self)
        if not pasta:
            return
        fpath = f"data/{pasta}/embeddings.pkl"
        if not os.path.exists(fpath):
            self.lift()
            messagebox.showerror("Erro", "Nenhum cadastro nessa pasta.", parent=self)
            return
        nomes = list({n.split("|")[0] for n, _ in pickle.load(open(fpath,'rb'))})
        self.lift()
        nome = simpledialog.askstring("Pessoa", f"Pessoas: {nomes}", parent=self)
        if nome:
            self.search_pasta, self.search_nome = pasta, nome
            self._set_mode("search")

    def _webcam_register(self):
        from cadastro_vivo import cadastro_vivo
        cadastro_vivo()

    def _on_click(self, e):
        if self.mode != "register":
            return
        for f in self.detected_faces:
            x1, y1, x2, y2 = f.bbox.astype(int)
            if x1 <= e.x <= x2 and y1 <= e.y <= y2:
                self.lift()
                nome = simpledialog.askstring("Nome", "Digite o nome da pessoa:", parent=self)
                if nome:
                    save_embedding(nome, f.embedding)
                break
        self._set_mode("general")

    def update_frame(self):
        # Reset diário
        today = date.today().isoformat()
        if today != self.current_date:
            self.current_date = today
            self.notified_today.clear()

        # Captura a tela de análise inteira
        mon = monitores[monitor_analise]
        region = {"left": mon.x, "top": mon.y, "width": mon.width, "height": mon.height}
        img = np.array(self.sct.grab(region))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        faces = face_app.get(frame)
        self.detected_faces = faces

        alert = None
        alert_box = None

        # Monitoramento
        if self.mode == "monitor":
            for nome, emb, p in load_all_embeddings():
                for f in faces:
                    sim = cosine_similarity([f.embedding], [emb])[0][0]
                    if sim >= 0.5:
                        nome_base, motivo = (nome.split("|", 1) + [""])[:2]
                        x1, y1, x2, y2 = f.bbox.astype(int)
                        color = (0, 0, 255) if p == "alerta" else (255, 0, 0)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(frame, nome_base, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                        if p == "alerta" and nome_base not in self.notified_today:
                            alert = ("warn", nome_base, motivo)
                            alert_box = (x1, y1, x2, y2)
                            self.notified_today.add(nome_base)

        # Busca
        elif self.mode == "search":
            embs = load_target_embeddings(self.search_pasta, self.search_nome)
            for f in faces:
                sim = max((cosine_similarity([f.embedding], [e])[0][0] for e in embs), default=0)
                if sim >= 0.5 and self.search_nome not in self.notified_today:
                    x1, y1, x2, y2 = f.bbox.astype(int)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, self.search_nome, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    alert = ("info", self.search_nome, None)
                    alert_box = (x1, y1, x2, y2)
                    self.notified_today.add(self.search_nome)

        # Geral
        if self.mode not in ("monitor", "search"):
            for f in faces:
                x1, y1, x2, y2 = f.bbox.astype(int)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Exibe no Canvas
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img_rgb).resize(
            (self.canvas.winfo_width(), self.canvas.winfo_height())
        )
        self.photo = ImageTk.PhotoImage(im)
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)

        # Captura e alerta
        if alert:
            typ, nome_base, motivo = alert
            x1, y1, x2, y2 = alert_box
            det_img = frame[y1:y2, x1:x2]
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"{DETECTIONS_FOLDER}/{nome_base}_{ts}.png"
            cv2.imwrite(fname, det_img)
            self.lift()
            if typ == "warn":
                messagebox.showwarning(
                    "🚨 Alerta",
                    f"{nome_base} detectado!\nMotivo: {motivo}\nSalvo em: {fname}",
                    parent=self
                )
            else:
                messagebox.showinfo(
                    "Encontrou",
                    f"{nome_base} detectado!\nSalvo em: {fname}",
                    parent=self
                )

        # Agenda próximo frame
        self.after(30, self.update_frame)


if __name__ == "__main__":
    app = App()
    app.mainloop()
```0