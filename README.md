<h1 align="center">
iBitter-Stack
</h1>

<h3 align="center">
A Multi-Representation Ensemble Learning Framework for Accurate Bitter Peptide Identification
</h3>

<div align="center">

[![Paper](https://img.shields.io/badge/Paper-arXiv-red)](https://arxiv.org/abs/2505.15730)
[![Web Server](https://img.shields.io/badge/Web%20Server-Streamlit-blue)](https://ibitter-stack-webserver.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)

</div>

---

## 📌 Overview

**iBitter-Stack** is a stacking-based ensemble learning framework for accurate classification of **Bitter vs. Non-Bitter peptides**.

The framework integrates:

- 🧬 Protein Language Model embeddings (ESM-2)
- ⚗️ Physicochemical descriptors (AAI, CTD, GTPC)
- 📊 Composition-based encodings (DPC, AAE, BPNC)
- 🤖 56 base learners (7 encodings × 8 classifiers)
- 🧠 Logistic Regression meta-learner

Unlike prior approaches that rely on a single embedding or fixed ensemble configuration, iBitter-Stack dynamically selects high-performing base learners and fuses their probability outputs into a meta-dataset for robust final prediction.

---

## 📄 Associated Paper

**iBitter-Stack: A Multi-Representation Ensemble Learning Model for Accurate Bitter Peptide Identification**  
Sarfraz Ahmad, Momina Ahsan, Muhammad Nabeel Asim, Andreas Dengel, Muhammad Imran Malik

📌 Preprint: https://arxiv.org/abs/2505.15730

📌 Journal Article: https://www.sciencedirect.com/science/article/abs/pii/S0022283625005145

---

## 📁 Repository Structure

```
backend/
│
├── app.py
├── predictor.py
├── model_loader.py
├── saved_models/
├── embeddings/
│   ├── esm.py
│   ├── aai.py
│   ├── ctd.py
├── static/
├── test.csv
└── requirements.txt
```

---

## 🧬 Method Overview

### 🔹 Dataset

**BTP640 Benchmark Dataset**

- 320 Bitter peptides
- 320 Non-Bitter peptides

**8:2 split:**

- Training: 512 peptides
- Independent Test: 128 peptides

An additional similarity-controlled experiment (80% identity threshold) confirms robustness.

### 🔹 Feature Representations (7 Types)

| Category          | Features                   |
| ----------------- | -------------------------- |
| Protein LM        | ESM-2 embeddings (320-dim) |
| Composition       | DPC                        |
| Position-based    | AAE                        |
| Terminal Encoding | BPNC                       |
| Physicochemical   | AAI                        |
| Distribution      | CTD                        |
| Grouped Motifs    | GTPC                       |

### 🔹 Base Learners

**8 classifiers × 7 encodings = 56 base models**

- SVM
- Random Forest
- Logistic Regression
- KNN
- Naive Bayes
- Decision Tree
- AdaBoost
- MLP

**Only models satisfying:**

- MCC > 0.80
- Accuracy > 90%

are selected for meta-learning.

### 🔹 Stacking Strategy

- Top 8 base learners selected
- Each outputs probability score
- Concatenated into 8D meta-vector
- Logistic Regression meta-learner produces final prediction

---

## 📊 Performance

### 🔹 Independent Test Set Results

| Model         | Accuracy  | Sensitivity | Specificity | MCC      | AUROC |
| ------------- | --------- | ----------- | ----------- | -------- | ----- |
| iBitter-Stack | **96.1%** | 95.4%       | 97.2%       | **0.92** | 0.98  |

### 🔹 After 80% Identity Filtering

| Model            | Accuracy | MCC  | AUROC |
| ---------------- | -------- | ---- | ----- |
| Filtered Dataset | 95.3%    | 0.91 | 0.98  |

### 🔹 Comparison with State-of-the-Art

| Model                        | Accuracy  | MCC      |
| ---------------------------- | --------- | -------- |
| iBitter-SCM                  | 84.0%     | 0.69     |
| BERT4Bitter                  | 92.2%     | 0.84     |
| iBitter-Fuse                 | 93.0%     | 0.86     |
| iBitter-DRLF                 | 94.0%     | 0.89     |
| UniDL4BioPep                 | 93.8%     | 0.87     |
| iBitter-GRE                  | 96.1%     | 0.92     |
| **iBitter-Stack (Proposed)** | **96.1%** | **0.92** |

---

## 🌐 Web Server

A real-time prediction interface is available at:

🔗 https://ibitter-stack-webserver.streamlit.app

**Features:**

- Single sequence prediction
- Batch CSV upload
- Base model probability visualization
- Confidence scoring

---

## 🚀 Installation

```bash
git clone https://github.com/SarfrazAhmad307/iBitter-Stack.git
cd iBitter-Stack
pip install -r requirements.txt
```

---

## 📚 Citation

If you use this repository or paper, please cite:

```bibtex
@article{AHMAD2025169448,
    title = {iBitter-Stack: A multi-representation ensemble learning model for accurate bitter peptide identification},
    journal = {Journal of Molecular Biology},
    volume = {437},
    number = {24},
    pages = {169448},
    year = {2025},
    issn = {0022-2836},
    doi = {https://doi.org/10.1016/j.jmb.2025.169448},
    url = {https://www.sciencedirect.com/science/article/pii/S0022283625005145},
    author = {Sarfraz Ahmad and Momina Ahsan and Muhammad Nabeel Asim and Andreas Dengel and Muhammad Imran Malik},
    keywords = {bitter peptides, bioinformatics, sequence classification, machine learning, protein language models, logistic regression},
}
```
