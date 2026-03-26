import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import subprocess
import os

from services.funções import *

st.set_page_config(layout="centered")


if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)


# carregar modelo apenas uma vez
@st.cache_resource
def carregar_modelo():
    return WhisperModel(
        "small",          # mais preciso que base
        compute_type="int8"
    )

model = carregar_modelo()


def converter_para_wav(entrada):
    base = os.path.splitext(entrada)[0]
    saida = base + "_convertido.wav"  # 👈 mudou aqui

    comando = [
        "ffmpeg",
        "-y",
        "-i", entrada,
        "-ac", "1",
        "-ar", "16000",
        saida
    ]

    subprocess.run(comando)

    return saida

st.title("Caixa360")


audio = st.audio_input("Comando por áudio")


if audio is not None:

    audio_bytes = audio.read()

    if not audio_bytes:
        st.error("Áudio vazio")
        st.stop()

    # detectar extensão
    tipo = audio.type
    extensao = tipo.split("/")[-1]

    # salvar audio temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extensao}") as f:
        f.write(audio_bytes)
        caminho_audio = f.name

    # converter para wav
    caminho_wav = converter_para_wav(caminho_audio)

    with st.spinner("Reconhecendo voz..."):

        segments, info = model.transcribe(
            caminho_wav,
            language="pt",        # força português
            beam_size=5           # melhora precisão
        )

        texto = ""

        for segment in segments:
            texto += segment.text

        texto = texto.strip()

    st.subheader("Texto reconhecido")

    if texto:
        st.write(texto)
        botao = st.button("Processar")
        if botao:
            with st.spinner("Processando..."):
                interpretar_comando(texto)


    else:
        st.warning("Não foi possível reconhecer o áudio.")

    