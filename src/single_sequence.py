import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

from predictor import final_prediction

VALID_AAS = set("ACDEFGHIKLMNPQRSTVWY")


def single_sequence(dark_mode: bool = False):
    st.markdown(
        "<p style='color:#555; margin-bottom:1rem;'>"
        "Enter a peptide sequence (standard amino acid letters) to predict whether it is "
        "<strong>Bitter</strong> or <strong>Non-Bitter</strong>.</p>",
        unsafe_allow_html=True,
    )

    col_input, _ = st.columns([3, 2])
    with col_input:
        sequence = st.text_input(
            "Peptide Sequence",
            value="",
            placeholder="e.g., IVY",
            label_visibility="visible",
        )

    sequence = sequence.upper().strip()

    if st.button("Predict", type="primary"):
        if not sequence:
            st.warning("Please enter a peptide sequence.")
            return

        invalid = set(sequence) - VALID_AAS
        if invalid:
            st.error(
                f"Invalid amino acid characters detected: **{', '.join(sorted(invalid))}**. "
                "Please use only standard single-letter amino acid codes (A–Y)."
            )
            return

        with st.spinner("Computing features and running ensemble…"):
            try:
                result = final_prediction(sequence)
            except Exception as e:
                st.error(f"Prediction failed: {e}")
                return

        pred = result["final_prediction"]
        conf = float(result["confidence"])

        if pred == "Bitter":
            st.markdown(
                f'<div class="pred-bitter">🔴 Prediction: <strong>Bitter</strong>'
                f' &nbsp;|&nbsp; Confidence: <strong>{conf:.2%}</strong></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="pred-nonbitter">🟢 Prediction: <strong>Non-Bitter</strong>'
                f' &nbsp;|&nbsp; Confidence: <strong>{conf:.2%}</strong></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Base learner probabilities
        base_probs = result["base_probs"]
        prob_df = pd.DataFrame.from_dict(
            base_probs, orient="index", columns=["Probability"]
        )
        prob_df.index.name = "Model"
        prob_df = prob_df.sort_values("Probability", ascending=True)

        detail_col, chart_col = st.columns([1, 2])

        with detail_col:
            st.markdown(
                "<p style='font-size:0.88rem; font-weight:600; color:#1a1a2e;"
                " margin-bottom:0.4rem;'>🔬 Base Model Probabilities</p>",
                unsafe_allow_html=True,
            )
            display_df = prob_df.copy()
            display_df.index = display_df.index.astype(str)
            display_df["Probability"] = display_df["Probability"].map(lambda x: f"{float(x):.4f}")
            st.dataframe(display_df, width="stretch")

        with chart_col:
            bg_color  = "#1a1f2e" if dark_mode else "#ffffff"
            fg_color  = "#e8eaf0" if dark_mode else "#1a1a2e"
            grid_color = "#2e3347" if dark_mode else "#eeeeee"

            fig, ax = plt.subplots(figsize=(6, 3.5))
            fig.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)

            bar_colors = [
                "#e05c4b" if float(v) >= 0.5 else "#2980b9"
                for v in prob_df["Probability"]
            ]
            prob_df["Probability"].astype(float).plot(
                kind="barh", ax=ax, color=bar_colors, edgecolor="none"
            )
            ax.set_xlabel("Probability", fontsize=9, color=fg_color)
            ax.set_xlim(0, 1)
            ax.axvline(0.5, color=fg_color, linewidth=0.8, linestyle="--", alpha=0.5)
            ax.tick_params(axis="both", labelsize=8, colors=fg_color)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            for spine in ["left", "bottom"]:
                ax.spines[spine].set_color(grid_color)
            ax.yaxis.label.set_color(fg_color)
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        st.caption(
            "Red bars indicate a bitter probability ≥ 0.5; blue bars indicate < 0.5. "
            "The dashed line marks the 0.5 decision threshold."
        )
