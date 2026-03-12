# import os
# import tempfile
# import streamlit as st
# from repo.caixa360_repo import *
# from faster_whisper import WhisperModel


# from services.funções import interpretar_comando


# os.environ["PATH"] += os.pathsep + r"C:\Users\luize\OneDrive\Ambiente de Trabalho\luiz\ffmpeg\ffmpeg\bin"

# st.set_page_config(layout="centered")


# if "logado" not in st.session_state:
#     st.session_state.logado = False

# if not st.session_state.logado:
#     st.markdown("""
#         <style>
#             [data-testid="stSidebar"] {
#                 display: none;
#             }
#         </style>
#     """, unsafe_allow_html=True)

# st.title("Caixa 360")

# model = WhisperModel("base", compute_type="int8")
# audio = st.audio_input("Fale algo")

# if audio is not None:
#      # pegar extensão real do audio
#     tipo = audio.type
#     extensao = tipo.split("/")[-1]

#     # salvar audio temporariamente
#     with tempfile.NamedTemporaryFile(delete=False, suffix=f".{extensao}") as f:
#         f.write(audio.getbuffer())
#         caminho_audio = f.name

#     # transcrever audio
#     segments, info = model.transcribe(caminho_audio)

#     texto = ""

#     for segment in segments:
#         texto += segment.text

#     st.write("Texto reconhecido:")
#     st.write(texto)
#     st.write(audio.type)

#     # botão para executar comando
#     if st.button("Executar comando"):
#         interpretar_comando(texto)





import streamlit as st
from faster_whisper import WhisperModel
import tempfile
import subprocess
import os

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


st.title("Assistente por áudio")

audio = st.audio_input("Grave um áudio")

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