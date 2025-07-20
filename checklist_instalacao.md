# 📋 Checklist de Instalação – face_id_lojas

Este checklist orienta técnicos e operadores a instalar, configurar e validar o sistema de reconhecimento facial usando telas do sistema SIM Next da Intelbras.

---

## 🛠️ 1. Requisitos do sistema

- [ ] Windows 10 ou superior
- [ ] Python 3.10+ instalado
- [ ] GPU dedicada (GTX 1650 ou superior) **ou** onnxruntime para CPU
- [ ] Driver da placa de vídeo atualizado
- [ ] Fonte de energia estável e bom sistema de refrigeração
- [ ] Tela principal conectada via HDMI ou DisplayPort

---

## 📂 2. Estrutura de pastas

- [ ] Baixar e descompactar a pasta `face_id_lojas`
- [ ] Confirmar que existem subpastas `data/`, `run.bat`, `main.py`, etc.

---

## 📦 3. Primeira execução

- [ ] Executar `run.bat` (Windows) ou `run.sh` (Linux/macOS)
- [ ] Ambiente virtual será criado automaticamente
- [ ] As dependências serão instaladas
- [ ] O menu principal será exibido

---

## 🖥️ 4. Configuração da entrada

- [ ] Escolher entre:
  - **Tela (monitor HDMI):** para usar câmera via DVR (ex: SIM Next)
  - **Webcam/USB:** caso conecte câmera diretamente
- [ ] Selecionar o monitor onde o vídeo será exibido
- [ ] Confirmar que a **interface gráfica aparece no monitor correto**

---

## 👤 5. Cadastro de pessoas

- [ ] Escolher entre:
  - Cadastro clicando no rosto da tela
  - Cadastro manual via imagens (arquivo `cadastro_manual.py`)
- [ ] Definir destino:
  - Nome da loja
  - Ou pasta especial `alerta` (com motivo obrigatório)

---

## 🔍 6. Modo "Procurar pessoa salva"

- [ ] Escolher a loja ou alerta
- [ ] Selecionar a pessoa da lista
- [ ] Exibir imagem da câmera (tela cheia do SIM Next)
- [ ] Confirmar que o sistema reconhece e:
  - Emite **bip**
  - Desenha **quadrado vermelho**
  - Abre janela com **horários detectados (OCR)**

---

## 🎛️ 7. Modo "Monitoramento"

- [ ] Exibir tela com mosaico de câmeras (SIM Next)
- [ ] Rodar `monitoramento.py`
- [ ] Confirmar:
  - Pessoas das lojas: nome com quadrado azul
  - Pessoas da pasta alerta: bip + pop-up com motivo
  - Nenhum rosto não cadastrado é desenhado

---

## 🧪 8. Testes finais

- [ ] Verificar detecção com diferentes ângulos e distâncias
- [ ] Simular reconhecimento de pessoa da pasta alerta
- [ ] Testar com OCR de hora (visível no canto superior do vídeo)
- [ ] Usar a opção “Alterar cadastro” para validar edição

---

## ✅ Pronto!

O sistema está operacional e pode ser usado pela equipe de segurança ou operadores.