import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Add backend path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

from predictor import final_prediction


def single_sequence():
    st.markdown(
        "Enter a peptide sequence to predict whether it's **Bitter** or **Non-Bitter**:"
    )
    sequence = st.text_input("Peptide Sequence", value="", placeholder="e.g., IVY")
    sequence = sequence.upper()

    if st.button("Predict"):
        if not sequence:
            st.warning("Please enter a sequence.")
        else:
            try:
                result = final_prediction(sequence)
                st.success(
                    f"✅ Prediction: **{result['final_prediction']}** (Confidence: {result['confidence']})"
                )

                st.markdown("#### 🔬 Model Probabilities")
                prob_df = pd.DataFrame([result["base_probs"]]).T
                prob_df.columns = ["Probability"]
                st.dataframe(prob_df)

                # Bar chart of model confidences
                st.markdown("#### 📊 Base Model Probabilities")
                fig, ax = plt.subplots()
                prob_df.plot(kind="barh", legend=False, ax=ax, color="skyblue")
                ax.set_xlabel("Probability")
                ax.set_xlim(0, 1)
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
