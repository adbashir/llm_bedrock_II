import streamlit as st
from PIL import Image
from llm_ui import run_llm_ui
from nonllm_ui import run_nonllm_ui

# Display logo
logo = Image.open("image.png")
st.image(logo, use_container_width=False, width=200, output_format='PNG')

# App title
st.title("TRITON INSIGHTS 2.0")

# Mode selector: LLM or NON LLM
option = st.radio("Choose query mode:", ["LLM", "NON LLM"])

if option == "LLM":
    run_llm_ui()
else:
    run_nonllm_ui()
