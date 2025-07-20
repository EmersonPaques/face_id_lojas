# 🧠 face_id_lojas

Reconhecimento facial com base de dados separada por loja ou alerta.  
Detecta rostos a partir de uma tela (HDMI, monitor) ou câmera, identifica pessoas previamente cadastradas, gera alertas e logs temporários de OCR.

---

## 📁 Estrutura do projeto

```
face_id_lojas/
├── main.py                  # Menu principal e seleção de entrada/vizualização
├── cadastro.py              # Cadastro clicando em rostos na tela
├── cadastro_manual.py       # Cadastro manual com múltiplas imagens
├── reconhecimento.py        # Reconhecimento geral (todas as lojas)
├── procurar_pessoa.py       # Procurar pessoa específica com OCR da hora
├── monitoramento.py         # Monitoramento com pop-up e alerta para pasta "alerta"
├── alterar_cadastro.py      # Opção para editar nomes e motivos de pessoas salvas
├── utils.py                 # Funções auxiliares e configuração de entrada/tela
├── requirements.txt         # Dependências do projeto
├── run.sh / run.bat         # Scripts de execução automática Linux / Windows
├── .gitignore               # Ignora venv, imagens e cache
└── data/
    ├── loja01/            # Exemplo de loja
    │   ├── funcionario_1.jpg
    │   ├── embeddings.pkl
    └── alerta/              # Pasta especial para pessoas com ocorrências
        ├── suspeito_1.jpg
        ├── embeddings.pkl
```

---

## 🚀 Como usar

### 🖥️ Escolha da entrada (ao iniciar)

O sistema irá perguntar:

1. Se deseja usar **tela (monitor HDMI)** ou **webcam/câmera USB** como fonte de verificação
2. Depois, qual **monitor usar para exibição da interface** (para não sobrepor a entrada)

---

## 🧭 Menu principal

```
1. Cadastrar nova pessoa
2. Iniciar reconhecimento
3. Procurar pessoa salva
4. Monitoramento (todas as pastas)
5. Alterar pessoa cadastrada
6. Sair
```

---

## 📝 Cadastro de pessoas

- **Loja:** salva em `data/{nome_da_loja}/`
- **Alerta:** salva em `data/alerta/` e pede **motivo da inclusão**

### Cadastro por:

- Tela HDMI (clicando em rostos)
- Múltiplas imagens (modo manual)

---

## 🔎 Procurar pessoa salva

- Escolhe a **pasta (loja ou alerta)**
- Lista pessoas ou motivos
- Sistema detecta **somente aquela pessoa**
- Ao detectar:
  - 🔴 Quadrado vermelho
  - 🔊 Bip de alerta
  - 🕒 OCR extrai hora do vídeo e mostra em janela
  - Botão para **copiar todos os registros de hora**

---

## 🛑 Monitoramento (modo geral)

- Verifica todas as pastas e rostos conhecidos
- Exibe:
  - 🔵 Quadrado azul + nome + nome da pasta (ex: `João - loja01`)
  - 🔴 Alerta com som + **pop-up com motivo** se estiver na pasta `alerta`

---

## ✏️ Alterar cadastro

- Escolhe loja ou alerta
- Lista pessoas salvas
- Permite:
  - Renomear pessoa
  - Alterar motivo (caso esteja na pasta `alerta`)

---

## 📌 Observações finais

- Nenhum rosto não cadastrado é desenhado (evita distração)
- Dados ficam 100% locais
- OCR funciona com timestamp visível em câmeras como Intelbras, Hikvision etc

---

## 👨‍💻 Autor

Desenvolvido por **Emerson Paques**  
Com apoio do ChatGPT + Python 🐍
