import os
import sounddevice as sd
import numpy as np
import subprocess
import requests
import json

import tempfile
from faster_whisper import WhisperModel

# Configurações
PIPER_EXE = "/usr/local/bin/piper/piper"
PIPER_MODEL = "/usr/local/bin/piper/pt_BR-faber-medium.onnx"
OLLAMA_MODEL = "mistral"
SAMPLE_RATE = 16000
DURACAO_GRAVACAO = 5  # segundos

# Carrega o Whisper (na primeira vez faz download do modelo)
print("Carregando Whisper...")
stt = WhisperModel(
    os.path.expanduser("~/whisper-models/tiny"),
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
    print('Estamos transcrevendo issaki')
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        nome = f.name
        import scipy.io.wavfile as wav
        wav.write(nome, SAMPLE_RATE, (audio * 32767).astype(np.int16))

    # Arquivo já fechado aqui, aí transcreve e deleta sem problema
    segments, _ = stt.transcribe(nome, language="pt")
    texto = " ".join([s.text for s in segments]).strip()
    os.unlink(nome)
    return texto


def perguntar_llm_streaming(mensagem):
    historico.append({"role": "user", "content": mensagem})
    resp = requests.post("http://localhost:11434/api/chat", json={
        "model": OLLAMA_MODEL,
        "messages": historico,
        "stream": True
    }, stream=True)

    resposta_completa = ""
    buffer = ""

    for linha in resp.iter_lines():
        if not linha:
            continue
        dados = json.loads(linha)
        if "error" in dados:
            print(f"[ERRO] {dados['error']}")
            historico.pop()
            return "Desculpe, ocorreu um erro."
        
        token = dados.get("message", {}).get("content", "")
        resposta_completa += token
        buffer += token

        # Fala quando termina uma frase
        if any(buffer.endswith(p) for p in [".", "!", "?", "\n"]):
            if buffer.strip():
                falar(buffer.strip())
            buffer = ""

    # Fala o que sobrou no buffer
    if buffer.strip():
        falar(buffer.strip())

    historico.append({"role": "assistant", "content": resposta_completa})
    return resposta_completa


def falar(texto):
    print("Jarvis:", texto)
    proc = subprocess.Popen(
        [PIPER_EXE, "--model", PIPER_MODEL, "--output-raw"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
    )
    audio_raw, _ = proc.communicate(input=texto.encode("utf-8"))
    audio_np = np.frombuffer(audio_raw, dtype=np.int16).astype(np.float32) / 32768
    sd.play(audio_np, samplerate=22050)
    sd.wait()

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
    resposta = perguntar_llm_streaming(texto)
    falar(resposta)