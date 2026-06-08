import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

from predictor import final_prediction

VALID_AAS = set("ACDEFGHIKLMNPQRSTVWY")


def batch_sequences():
    st.markdown(
        "<p style='color:#555; margin-bottom:0.5rem;'>"
        "Upload a CSV file with a column named <code>sequence</code> containing peptide sequences. "
        "All sequences will be processed by the ensemble model and results can be downloaded.</p>",
        unsafe_allow_html=True,
    )

    # Example download
    example_csv = "sequence\nIVY\nALF\nPGP\nRFP\nVD"
    st.download_button(
        label="📄 Download Example CSV",
        data=example_csv,
        file_name="example_peptides.csv",
        mime="text/csv",
    )

    uploaded_file = st.file_uploader(
        "Upload Peptide Sequences CSV",
        type=["csv"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:
        st.info("Upload a CSV file to begin batch prediction.")
        return

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        return

    if "sequence" not in df.columns:
        st.error(
            "❌ CSV must contain a column named `sequence`. "
            f"Found columns: {list(df.columns)}"
        )
        return

    sequences = df["sequence"].dropna().str.upper().str.strip().tolist()
    if not sequences:
        st.warning("No sequences found in the uploaded file.")
        return

    st.markdown(
        f"<p style='font-size:0.9rem; color:#555;'>Found <strong>{len(sequences)}</strong> sequence(s). Running predictions…</p>",
        unsafe_allow_html=True,
    )

    progress = st.progress(0, text="Starting…")
    results = []
    errors = []

    for i, seq in enumerate(sequences):
        invalid = set(seq) - VALID_AAS
        if invalid:
            errors.append(f"Row {i+1} ('{seq}'): invalid characters {sorted(invalid)}")
            results.append({
                "sequence": seq,
                "final_prediction": "Error",
                "confidence": "",
                "base_probs": {},
            })
        else:
            try:
                r = final_prediction(seq)
                r["sequence"] = seq
                results.append(r)
            except Exception as e:
                errors.append(f"Row {i+1} ('{seq}'): {e}")
                results.append({
                    "sequence": seq,
                    "final_prediction": "Error",
                    "confidence": str(e),
                    "base_probs": {},
                })

        progress.progress((i + 1) / len(sequences), text=f"Processing {i+1}/{len(sequences)}…")

    progress.empty()

    if errors:
        with st.expander(f"⚠️ {len(errors)} sequence(s) had errors"):
            for err in errors:
                st.write(f"- {err}")

    result_df = pd.DataFrame(results)

    # Flatten base_probs dict into columns
    if "base_probs" in result_df.columns:
        probs_df = result_df["base_probs"].apply(pd.Series)
        probs_df.columns = [f"prob_{c}" for c in probs_df.columns]
        result_df = pd.concat(
            [result_df[["sequence", "final_prediction", "confidence"]], probs_df],
            axis=1,
        )

    result_df = result_df.astype(str)

    # Summary
    n_bitter = (result_df["final_prediction"] == "Bitter").sum()
    n_nonbitter = (result_df["final_prediction"] == "Non-Bitter").sum()
    n_error = (result_df["final_prediction"] == "Error").sum()

    c1, c2, c3 = st.columns(3)
    c1.metric("Bitter", n_bitter)
    c2.metric("Non-Bitter", n_nonbitter)
    if n_error:
        c3.metric("Errors", n_error)

    st.success("✅ Predictions complete!")
    st.dataframe(result_df, width="stretch")

    csv_out = result_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Predictions as CSV",
        data=csv_out,
        file_name="ibitter_stack_predictions.csv",
        mime="text/csv",
    )
