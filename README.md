# 🤖 Assistente Virtual Local (Jarvis) - Documentação

## 📌 Visão Geral

Este projeto consiste em um assistente virtual local capaz de:

* Ouvir comandos de voz
* Transcrever fala para texto
* Processar linguagem natural com IA local
* Responder com voz

Tudo roda **100% offline**, sem consumo de APIs pagas.

---

## 🧠 Arquitetura do Sistema

Fluxo principal:

1. Microfone captura áudio
2. Whisper (STT) converte voz → texto
3. LLM (Ollama) processa a mensagem
4. TTS converte texto → voz

---

## 🧩 Tecnologias Utilizadas

### 1. Speech-to-Text (STT)

* faster-whisper

### 2. LLM (Inteligência Artificial)

* Ollama
* Modelo utilizado: mistral (ou phi3 recomendado)

### 3. Text-to-Speech (TTS)

* pyttsx3 (offline)

### 4. Outras bibliotecas

* requests
* pyaudio
* numpy
* sounddevice (opcional)

---

## 📦 Instalação das Dependências

### 🔹 Python

Versão recomendada: **Python 3.10+**

---

### 🔹 Instalar bibliotecas Python

```bash
pip install faster-whisper
pip install requests
pip install pyttsx3
pip install pyaudio
pip install numpy
```

---

## 🧠 Instalação do Ollama

1. Baixar: [https://ollama.com](https://ollama.com)
2. Instalar normalmente

---

## 📥 Baixar Modelo de IA

```bash
ollama pull mistral
```

OU (recomendado para performance):

```bash
ollama pull phi3
```

---

## ▶️ Iniciar o Servidor de IA

```bash
ollama serve
```

A API ficará disponível em:

```
http://localhost:11434
```

---

## 🎤 Modelos Whisper (Offline)

Você precisa baixar manualmente um modelo do faster-whisper.

### Estrutura esperada:

```
whisper-models/
 └── base/
     ├── config.json
     ├── model.bin
     ├── vocabulary.json
     └── merges.txt
```

---

## ⚙️ Configuração do Projeto

No código Python, configure:

### Modelo do Ollama:

```python
"model": "mistral"
```

ou

```python
"model": "phi3"
```

---

### Caminho do Whisper:

```python
WhisperModel("C:/whisper-models/base")
```

---

## 🚀 Como Executar

1. Iniciar Ollama:

```bash
ollama serve
```

2. Rodar o assistente:

```bash
python assistente.py
```

---

## ⚠️ Possíveis Problemas

### ❌ Erro: conexão recusada (porta 11434)

* Ollama não está rodando

### ❌ Erro: modelo não encontrado

* Executar:

```bash
ollama pull mistral
```

### ❌ Erro: FileNotFoundError (voz)

* Verificar instalação do pyttsx3

---

## ⚡ Melhorias Futuras

* Ativação por palavra-chave ("Jarvis")
* Integração com comandos do sistema (abrir apps)
* Voz mais natural (Coqui TTS)
* Interface gráfica
* Memória de contexto

---

## 📁 Estrutura do Projeto

```
projeto/
 ├── assistente.py
 ├── requisitos.txt
 └── whisper-models/
```

---

## 📄 requirements.txt (sugestão)

```
faster-whisper
requests
pyttsx3
pyaudio
numpy
```

---

## 🧠 Observações

* O desempenho depende do hardware
* Modelos menores = mais rápidos
* Tudo roda localmente (sem internet após setup)

---

## 👨‍💻 Autor

Projeto desenvolvido para estudo de IA local e automação.
