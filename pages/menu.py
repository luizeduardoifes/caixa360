import os
import tempfile
import streamlit as st
from repo.caixa360_repo import *
import whisper

from services.funções import interpretar_comando


os.environ["PATH"] += os.pathsep + r"C:\Users\luize\OneDrive\Ambiente de Trabalho\luiz\ffmpeg\ffmpeg\bin"

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

model = whisper.load_model("base")


audio = st.audio_input("Fale algo")
input_text = st.text_input("Ou digite algo")

if audio:
     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            f.write(audio.read())
            caminho_audio = f.name
            result = model.transcribe(caminho_audio)
            comando = result["text"]

            interpretar_comando(comando)











    
