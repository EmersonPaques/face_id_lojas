
import cv2
import mss
from screeninfo import get_monitors

CONFIG = {
    "entrada": None,
    "monitor_entrada": None,
    "monitor_exibicao": None,
    "camera_index": None
}

def selecionar_entrada_e_tela():
    print("Selecione a fonte de entrada:")
    print("1. Tela (monitor HDMI, por exemplo)")
    print("2. Webcam ou câmera USB")

    while True:
        tipo = input("Digite 1 ou 2: ").strip()
        if tipo in ["1", "2"]:
            break
        print("Opção inválida. Tente novamente.")

    if tipo == "1":
        CONFIG["entrada"] = "monitor"
        monitores = get_monitors()
        print("\nMonitores disponíveis:")
        for i, m in enumerate(monitores):
            print(f"{i + 1}. Monitor {i + 1}: {m.width}x{m.height} at {m.x},{m.y}")
        while True:
            idx = input("Escolha o número do monitor de entrada (onde a câmera está exibindo): ")
            if idx.isdigit() and 1 <= int(idx) <= len(monitores):
                CONFIG["monitor_entrada"] = int(idx) - 1
                break
            print("Escolha inválida.")
    else:
        CONFIG["entrada"] = "camera"
        print("\nCâmeras disponíveis:")
        for i in range(5):
            cap = cv2.VideoCapture(i)
            if cap.read()[0]:
                print(f"{i}. Câmera {i} detectada")
                cap.release()
        while True:
            idx = input("Digite o número da câmera que deseja usar: ")
            if idx.isdigit():
                CONFIG["camera_index"] = int(idx)
                break
            print("Escolha inválida.")

    # Escolher onde exibir a interface
    monitores = get_monitors()
    print("\nOnde você deseja exibir a aplicação?")
    for i, m in enumerate(monitores):
        print(f"{i + 1}. Monitor {i + 1}: {m.width}x{m.height} at {m.x},{m.y}")
    while True:
        idx = input("Escolha o número do monitor de exibição: ")
        if idx.isdigit() and 1 <= int(idx) <= len(monitores):
            CONFIG["monitor_exibicao"] = int(idx) - 1
            break
        print("Escolha inválida.")

    return CONFIG

def get_monitor_region(index):
    monitores = get_monitors()
    m = monitores[index]
    return {"top": m.y, "left": m.x, "width": m.width, "height": m.height}
