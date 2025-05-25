<!--
title: iBitter-Stack
emoji: 🧪
colorFrom: green
colorTo: purple
sdk: streamlit
app_file: src/app.py
pinned: false
-->

# iBitter-Stack 🧪

This repository provides a powerful backend for predicting whether peptide sequences are **Bitter** or **Non-Bitter**, using a combination of multiple machine learning models and a meta-classifier.

## 🚀 Features

- Predict from a single sequence (via terminal)
- Predict from a CSV file (batch mode)
- Embedding support: ESM, AAI, CTD
- Meta-model: Logistic Regression
- Outputs include per-model probabilities + final result

---

## 🧰 Requirements

- Python 3.8+
- pip or conda

### 📦 Install dependencies

```bash
pip install -r requirements.txt
```

Or create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use: .\env\Scripts\activate
pip install -r requirements.txt
```

---

## 🧪 Run Single Sequence Prediction

Use the command line to predict bitterness of a single sequence:

```bash
python predictor.py <sequence>
```

### ✅ Example

```bash
python predictor.py IVY
```

You will receive a JSON output like this:

```json
{
    "base_probs": {
        "AAI_RF": 0.87,
        "CTD_MLP": 0.99,
        "CTD_SVM": 0.83,
        ...
    },
    "final_prediction": "Bitter",
    "confidence": 0.9867
}
```

---

## 📄 Run Batch Prediction (CSV)

Prepare a `.csv` file with a column called `sequence`, like this:

```csv
sequence
IVY
GLL
DFR
KQY
```

Then, run the FastAPI server:

```bash
uvicorn app:app --reload
```

In a **separate terminal**, run the prediction using `curl`:

```bash
curl -X POST -F "file=@test.csv" http://localhost:8000/predict/batch
```

You’ll receive an array of predictions, one for each sequence.

---

## 📂 Directory Structure

```
backend/
│
├── app.py                 # FastAPI entrypoint
├── predictor.py           # Prediction logic
├── model_loader.py        # Loads trained models
├── saved_models/          # Your 8 models + logistic regression
├── embeddings/
│   ├── esm.py             # ESM embeddings
│   ├── aai.py             # AAI embeddings
│   └── ctd.py             # CTD embeddings
├── static/                # Pipeline image (optional)
├── test.csv               # Example input CSV
└── requirements.txt       # Python dependencies
```

---

## Author

Built by Sarfraz Ahmad as part of a research on peptide bitterness prediction.

---

## 📬 Questions or Help?

Open an issue or reach out via `sarfaraz_076@outlook.com`.
