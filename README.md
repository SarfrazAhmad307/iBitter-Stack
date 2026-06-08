<div align="center">

# iBitter-Stack

<strong>A Multi-Representation Ensemble Learning Model for Accurate Bitter Peptide Identification</strong>

<sub>Sarfraz Ahmad<sup>1</sup> · Momina Ahsan<sup>1</sup> · Muhammad Nabeel Asim<sup>2</sup> · Andreas Dengel<sup>2</sup> · Muhammad Imran Malik<sup>1</sup></sub>

<sub><sup>1</sup> NUST, Islamabad, Pakistan &nbsp;·&nbsp; <sup>2</sup> DFKI, Kaiserslautern, Germany</sub>

<br>

[![Paper](https://img.shields.io/badge/Journal%20of%20Molecular%20Biology-2025-c0392b?style=flat-square&logo=elsevier&logoColor=white)](https://doi.org/10.1016/j.jmb.2025.169448)
[![arXiv](https://img.shields.io/badge/arXiv-2505.15730-b31b1b?style=flat-square&logo=arxiv&logoColor=white)](https://arxiv.org/abs/2505.15730)
[![Web Server](https://img.shields.io/badge/Web%20Server-Live-2ecc71?style=flat-square&logo=streamlit&logoColor=white)](https://ibitter-stack-webserver.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776ab?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-GPL-lightgrey?style=flat-square)](LICENSE)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Method](#method)
- [Results](#results)
- [Web Server](#web-server)
- [Installation](#installation)
- [Repository Structure](#repository-structure)
- [Citation](#citation)

---

## Overview

**iBitter-Stack** is a two-tier stacking ensemble that classifies peptide sequences as **Bitter** or **Non-Bitter**. It constructs 56 base learners by pairing 7 feature representations with 8 classifiers, selects the top performers by strict quality thresholds, and fuses their soft-probability outputs into a compact meta-dataset consumed by a Logistic Regression meta-learner.

Key design choices:

- Combines deep protein language model (ESM-2) embeddings with handcrafted physicochemical and compositional descriptors
- Dynamic base learner selection (MCC > 0.80, Accuracy > 90%) rather than a fixed configuration
- Meta-level fusion via soft probabilities — avoids feature redundancy from early concatenation

---

## Method

<details>
<summary><strong>Dataset — BTP640</strong></summary>

<br>

| Split                     | Bitter  | Non-Bitter | Total   |
| ------------------------- | ------- | ---------- | ------- |
| Training (BTP-CV)         | 256     | 256        | 512     |
| Independent Test (BTP-TS) | 64      | 64         | 128     |
| **Total**                 | **320** | **320**    | **640** |

- Bitter peptides collected from peer-reviewed experimental studies
- Non-bitter peptides randomly sampled from the [BIOPEP database](http://www.uwm.edu.pl/biochemia/index.php/pl/biopep)
- Peptides with ambiguous residues (X, B, U, Z) and 100%-identity duplicates removed
- Additional experiment with 80% identity threshold confirms robustness (Acc: 95.3%, MCC: 0.91)

</details>

<details>
<summary><strong>Feature Representations (7 types)</strong></summary>

<br>

| Feature                                   | Dimensions | Category               |
| ----------------------------------------- | ---------- | ---------------------- |
| ESM-2 `esm2_t6_8M_UR50D`                  | 320        | Protein language model |
| Dipeptide Composition (DPC)               | 400        | Compositional          |
| Amino Acid Entropy (AAE)                  | 60         | Positional             |
| Binary Profile N/C-terminus (BPNC)        | 200        | Positional             |
| Amino Acid Index (AAI)                    | 36         | Physicochemical        |
| Global Tripeptide Composition (GTPC)      | 125        | Physicochemical        |
| Composition-Transition-Distribution (CTD) | 147        | Physicochemical        |

</details>

<details>
<summary><strong>Base Learners &amp; Selection</strong></summary>

<br>

**7 features × 8 classifiers = 56 base models**, each trained with 10-fold cross-validation.

Classifiers: SVM · Random Forest · Logistic Regression · KNN · Naive Bayes · Decision Tree · AdaBoost · MLP

**Selection threshold:** MCC > 0.80 and Accuracy > 90%

Eight models qualify and contribute to the meta-dataset:

| Model   | CV Accuracy | CV MCC |
| ------- | ----------- | ------ |
| ESM_SVM | 85.5%       | 0.71   |
| ESM_RF  | 83.4%       | 0.67   |
| ESM_MLP | 83.6%       | 0.67   |
| ESM_LR  | 83.6%       | 0.67   |
| ESM_ADA | 83.0%       | 0.66   |
| CTD_MLP | 81.1%       | 0.62   |
| CTD_SVM | 83.2%       | 0.66   |
| AAI_RF  | 78.5%       | 0.57   |

</details>

<details>
<summary><strong>Stacking Architecture</strong></summary>

<br>

```
Peptide Sequence
      │
      ├─── ESM-2 ──────────────────────────────┐
      ├─── DPC  ────── [8 classifiers each] ───┤
      ├─── AAE  ─────────────────────────────  ├──► Select top 8 ──► 8D probability vector
      ├─── BPNC ─────────────────────────────  │
      ├─── AAI  ─────────────────────────────  │
      ├─── GTPC ─────────────────────────────  │
      └─── CTD  ──────────────────────────────┘
                                                │
                               Logistic Regression meta-learner
                                                │
                                    Bitter / Non-Bitter + confidence
```

The meta-learner is Logistic Regression (L2 penalty, `max_iter=1500`), chosen for its strong empirical performance in ensemble stacking scenarios and computational efficiency at inference time.

</details>

---

## Results

### Independent Test Set

| Metric      | Value     |
| ----------- | --------- |
| Accuracy    | **96.1%** |
| Sensitivity | 95.4%     |
| Specificity | **97.2%** |
| MCC         | **0.922** |
| AUROC       | **0.981** |

### Comparison with State-of-the-Art

| Predictor                | Year     | Accuracy  | Sensitivity | Specificity | MCC      | AUROC    |
| ------------------------ | -------- | --------- | ----------- | ----------- | -------- | -------- |
| iBitter-SCM              | 2020     | 84.0%     | 84.0%       | 84.0%       | 0.69     | 0.90     |
| BERT4Bitter              | 2021     | 92.2%     | 93.8%       | 90.6%       | 0.84     | 0.96     |
| iBitter-Fuse             | 2021     | 93.0%     | 94.0%       | 92.0%       | 0.86     | 0.93     |
| iBitter-DRLF             | 2022     | 94.0%     | 92.0%       | 96.9%       | 0.89     | 0.97     |
| UniDL4BioPep             | 2023     | 93.8%     | 92.4%       | 95.2%       | 0.87     | 0.98     |
| Bitter-RF                | 2023     | 94.0%     | 94.0%       | 94.0%       | 0.88     | 0.98     |
| iBitter-GRE              | 2025     | 96.1%     | 98.4%       | 93.8%       | 0.92     | 0.97     |
| **iBitter-Stack (Ours)** | **2025** | **96.1%** | **95.4%**   | **97.2%**   | **0.92** | **0.98** |

> iBitter-Stack achieves the highest specificity (97.2%) among all models and a more balanced sensitivity-specificity trade-off than iBitter-GRE (98.4% / 93.8%), indicating better control over both false positives and false negatives.

---

## Web Server

A real-time prediction interface is available at **[ibitter-stack-webserver.streamlit.app](https://ibitter-stack-webserver.streamlit.app)**.

Features:

- Single sequence prediction with confidence score
- Batch CSV upload for high-throughput screening
- Per-base-learner probability visualisation
- Downloadable results

---

## Installation

```bash
git clone https://github.com/SarfrazAhmad307/iBitter-Stack.git
cd iBitter-Stack
pip install -r requirements.txt
streamlit run src/app.py
```

---

## Repository Structure

```
iBitter-Stack/
├── src/
│   ├── app.py                  # Streamlit web application
│   ├── single_sequence.py      # Single sequence prediction UI
│   └── batch_sequences.py      # Batch upload UI
├── backend/
│   ├── predictor.py            # Ensemble inference pipeline
│   ├── model_loader.py         # Saved model loader
│   └── embeddings/
│       ├── esm.py              # ESM-2 feature extractor
│       ├── aai.py              # AAI feature extractor
│       └── ctd.py              # CTD feature extractor
├── data/                       # Dataset files
├── requirements.txt
└── README.md
```

---

## Citation

If you use iBitter-Stack in your research, please cite:

```bibtex
@article{ahmad2025ibitter,
  title     = {iBitter-Stack: A multi-representation ensemble learning model
               for accurate bitter peptide identification},
  author    = {Ahmad, Sarfraz and Ahsan, Momina and Asim, Muhammad Nabeel
               and Dengel, Andreas and Malik, Muhammad Imran},
  journal   = {Journal of Molecular Biology},
  volume    = {437},
  number    = {24},
  pages     = {169448},
  year      = {2025},
  publisher = {Elsevier},
  doi       = {10.1016/j.jmb.2025.169448},
  url       = {https://www.sciencedirect.com/science/article/pii/S0022283625005145}
}
```

---

<div align="center">
<sub>
Published in <em>Journal of Molecular Biology</em>, 437(24), 169448 (2025) &nbsp;·&nbsp;
<a href="https://doi.org/10.1016/j.jmb.2025.169448">DOI: 10.1016/j.jmb.2025.169448</a>
</sub>
</div>
