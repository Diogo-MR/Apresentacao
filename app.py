import streamlit as st
import os

st.set_page_config(page_title="Apresentação Reforma Tributária", layout="wide")

st.markdown("""
    <style>
        .stSlider > div { padding-left: 2rem; padding-right: 2rem; }
        .slide-frame iframe { border: none; width: 100%; height: 1000px; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Apresentação Interativa - Reforma Tributária")
st.subheader("FH Souza Advogados")

# Lista de slides (ordem exata)
slides = [
    "slide1.html",
    "slide2.html",
    "slide3.html",
    "slide4.html",
    "slide5.html",
    "slide6.html",
    "slide7.html"
]

slide_index = st.slider("Navegar pelos slides", 0, len(slides) - 1, 0,
                        format="%d", label_visibility="visible")

slide_file = slides[slide_index]

# Caminho completo
if not os.path.exists(slide_file):
    st.error(f"Slide {slide_file} não encontrado.")
else:
    with open(slide_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=1000, scrolling=True)
