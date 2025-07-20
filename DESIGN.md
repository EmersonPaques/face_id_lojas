# 🧠 DESIGN TÉCNICO – Projeto face_id_lojas

Este documento descreve a lógica, estrutura e decisões técnicas do projeto **face_id_lojas**, com o objetivo de facilitar futuras manutenções, refatorações ou migrações para outras plataformas (ex: app com GUI).

---

## 🗂️ Visão geral

O sistema realiza **reconhecimento facial local**, com **base de dados separada por loja**, e um modo especial para **alerta de pessoas suspeitas**.

A entrada pode vir de:

- Uma **câmera USB**
- Uma **tela HDMI** que exibe um DVR (ex: Intelbras SIM Next)

Todos os rostos salvos são mantidos em uma estrutura simples de arquivos.

---

## 🧱 Estrutura de arquivos

```
face_id_lojas/
├── main.py                # Menu principal + seleção de entrada/monitor
├── cadastro.py            # Cadastro clicando no rosto exibido em tela
├── cadastro_manual.py     # Cadastro por múltiplas imagens
├── procurar_pessoa.py     # Busca uma pessoa específica e extrai OCR da hora
├── monitoramento.py       # Exibe rostos conhecidos e alerta pop-up para pasta "alerta"
├── alterar_cadastro.py    # Permite editar nome ou motivo de um cadastro
├── utils.py               # Utilitários: embeddings, entrada, monitores
├── requirements.txt
├── config.json            # Salva configuração da entrada/monitor
└── data/
    ├── mixitaim/          # Exemplo de loja
    └── alerta/            # Pessoas com alerta (ex: suspeitos, ocorrências)
```

---

## 📇 Cadastro de pessoas

### `cadastro.py`
- Captura imagem da **tela ou câmera**
- Detecta rostos com `insightface`
- Usuário **clica no rosto**
- Sistema pergunta:
  - Nome da pessoa
  - Loja ou "alerta"
  - (Se alerta) motivo da inclusão
- Embedding é salvo em `data/{pasta}/embeddings.pkl` junto com imagens

### `cadastro_manual.py`
- Seleciona várias imagens JPG da pessoa
- Extrai embedding de cada uma
- Salva da mesma forma acima

---

## 🧠 Reconhecimento facial

### Vetores
- Usa `insightface` para gerar **embeddings** (vetores 512D)
- Compara usando **similaridade cosseno**
- Um rosto é reconhecido se a similaridade for maior que 0.5

### Pastas
- Cada pasta (`mixitaim`, `alerta`, etc) tem seu `embeddings.pkl` com lista de tuplas:
  ```python
  [("nome_da_pessoa|motivo", embedding_vector), ...]
  ```

---

## 🔍 Modo: Procurar pessoa salva

- Usuário escolhe:
  - A pasta (ex: `mixitaim`, `alerta`)
  - A pessoa ou motivo
- O sistema reconhece apenas essa pessoa
- Quando detectada:
  - Desenha 🔴 quadrado vermelho
  - Toca som de bip
  - Extrai **hora da filmagem** via OCR e exibe numa janela
  - Permite copiar os horários

---

## 🛡️ Modo: Monitoramento geral

- Verifica todas as pastas
- Rosto reconhecido:
  - Se de **loja comum** → 🔵 quadrado azul com nome e nome da loja
  - Se da pasta **alerta**:
    - 🔴 quadrado vermelho
    - Bip
    - Pop-up com **motivo da inclusão**

---

## ✏️ Alterar cadastro

- Lista todas as pessoas da pasta
- Permite:
  - Renomear
  - Editar o motivo (caso esteja na pasta `alerta`)
- Atualiza o `embeddings.pkl`

---

## 🧾 Dados

- Não usa banco de dados
- Tudo fica em:
  - Arquivo `embeddings.pkl` por pasta
  - Imagens `*.jpg` de cada pessoa (opcional, mais visual)
  - `config.json`: entrada usada e tela de exibição

---

## 🎯 Futuras melhorias previstas

- Interface gráfica com botões (Tkinter, PyQt ou web)
- Migração para app (desktop/mobile) com interface amigável
- Inclusão de reconhecimento em múltiplas regiões simultâneas
- Exportação de logs com horários detectados
- Upload automático para servidor (opcional)

---

## 👤 Desenvolvido por

**Emerson Paques** (usuário principal)Projeto guiado com suporte técnico do ChatGPT – Julho 2025