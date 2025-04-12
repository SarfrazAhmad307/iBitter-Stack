import streamlit as st
import pandas as pd
import torch
import sys
import os
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from single_sequence import single_sequence
from batch_sequences import batch_sequences

os.environ["TORCH_DISABLE_RELOADER"] = "1"

# Remove torch.classes error for Streamlit reload
if "torch.classes" in sys.modules:
    del sys.modules["torch.classes"]

# Add backend path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

from predictor import final_prediction

st.set_page_config(
    page_title="Bitter Peptide Predictor",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# st.title("🧪 Bitter Peptide Predictor")
st.markdown(
    "<h2 style='text-align: center;'>Bitter Peptide Predictor 🧪 </h2>",
    unsafe_allow_html=True,
)

st.markdown(
    "<h5 style='text-align: center;'>This web app predicts whether a peptide sequence is Bitter or Non-Bitter using a trained model.</h5>",
    unsafe_allow_html=True,
)

selected = option_menu(
    menu_title=None,
    options=["Single Sequence", "Batch Upload", "Algorithm", "About"],
    icons=[
        "bi bi-file-earmark-text",
        "bi bi-file-earmark-spreadsheet",
        "bi bi-gear",
        "bi bi-info-circle",
    ],
    default_index=0,
    orientation="horizontal",
)

if selected == "Single Sequence":
    single_sequence()
elif selected == "Batch Upload":
    batch_sequences()
elif selected == "Algorithm":
    st.markdown(
        "<h5 style='text-align: center;'>Algorithm Overview</h5>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h5 style='text-align: center;'>The Bitter Peptide Predictor uses a trained model to predict whether a peptide sequence is Bitter or Non-Bitter.</h5>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # add image
        st.image(
            "static/pipeline.png",
            # caption="Algorithm Overview",
            use_container_width=True,
        )
