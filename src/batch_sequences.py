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


def batch_sequences():
    uploaded_file = st.file_uploader("Upload your peptide sequences CSV", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            if "sequence" not in df.columns:
                st.error("❌ Your CSV must contain a column named `sequence`.")
            else:
                results = []
                for seq in df["sequence"]:
                    result = final_prediction(seq)
                    result["sequence"] = seq
                    results.append(result)

                result_df = pd.DataFrame(results)
                # Convert to object dtype to avoid PyArrow LargeUtf8 compatibility issues
                result_df = result_df.astype(str)

                st.success("✅ Predictions complete!")
                st.dataframe(result_df, use_container_width=True)

                # Download predictions
                csv = result_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Predictions as CSV",
                    data=csv,
                    file_name="bitter_predictions.csv",
                    mime="text/csv",
                )

        except Exception as e:
            st.error(f"Something went wrong: {e}")
