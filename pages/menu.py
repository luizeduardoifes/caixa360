import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import subprocess
import os

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

st.title("Caixa 360")


@st.cache_resource
def carregar_modelo():
    return WhisperModel("base", compute_type="int8")

model = carregar_modelo()

def converter_para_wav(entrada):
    base = os.path.splitext(entrada)[0]
    saida = base + ".wav"

    comando = [
        "ffmpeg",
        "-y",
        "-i",
        entrada,
        saida
    ]

    subprocess.run(comando)

    return saida

audio = st.audio_input("Áudio")

if audio is not None:

    audio_bytes = audio.read()

    if len(audio_bytes) == 0:
        st.error("Áudio vazio")
        st.stop()

    tipo = audio.type
    extensao = tipo.split("/")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extensao}") as f:
        f.write(audio_bytes)
        caminho_audio = f.name

    caminho_wav = converter_para_wav(caminho_audio)

    segments, info = model.transcribe(caminho_wav)

    texto = ""

    for segment in segments:
        texto += segment.text

    st.write("Texto reconhecido:")
    st.write(texto)