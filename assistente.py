import sounddevice as sd
import numpy as np
import subprocess
import requests
import json
import pyttsx3

import tempfile
import os
from faster_whisper import WhisperModel

# Configurações
PIPER_EXE = r"C:\piper\piper.exe"          # ajuste o caminho
PIPER_MODEL = r"C:\piper\faber-medium.onnx" # ajuste o caminho
OLLAMA_MODEL = "llama3.1"
SAMPLE_RATE = 16000
DURACAO_GRAVACAO = 5  # segundos

# Carrega o Whisper (na primeira vez faz download do modelo)
print("Carregando Whisper...")
stt = WhisperModel(
    r"C:\whisper-models\base",
    device="cpu",
    compute_type="int8"
)

historico = []

def gravar_audio():
    print("\n🎤 Fala agora...")
    audio = sd.rec(int(DURACAO_GRAVACAO * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    print('Aguarde..')
    return audio.flatten()


def transcrever(audio):
    print('Estamos transcrevendo issaki'
          '')
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        nome = f.name
        import scipy.io.wavfile as wav
        wav.write(nome, SAMPLE_RATE, (audio * 32767).astype(np.int16))

    # Arquivo já fechado aqui, aí transcreve e deleta sem problema
    segments, _ = stt.transcribe(nome, language="pt")
    texto = " ".join([s.text for s in segments]).strip()
    os.unlink(nome)
    return texto


def perguntar_llm(mensagem):
    historico.append({"role": "user", "content": mensagem})
    resp = requests.post("http://localhost:11434/api/chat", json={
        "model": "mistral",
        "messages": historico,
        "stream": False
    })
    dados = resp.json()
    if "error" in dados:
        print(f"[ERRO do Ollama] {dados['error']}")
        historico.pop()  # remove a mensagem que falhou
        return "Desculpe, ocorreu um erro ao processar sua mensagem."
    resposta = dados["message"]["content"]
    historico.append({"role": "assistant", "content": resposta})
    return resposta

engine = pyttsx3.init()

def falar(texto):
    print("Jarvis:", texto)
    engine.say(texto)
    engine.runAndWait()

# Loop principal
print("✅ Assistente pronto! Pressione Enter para falar, Ctrl+C para sair.\n")
while True:
    input("[ Enter para falar ]")
    audio = gravar_audio()
    texto = transcrever(audio)
    if not texto:
        print("(não entendi, tente novamente)")
        continue
    print(f"Você: {texto}")
    resposta = perguntar_llm(texto)
    falar(resposta)