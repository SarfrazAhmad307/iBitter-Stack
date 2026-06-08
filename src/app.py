import streamlit as st
import sys
import os

os.environ["TORCH_DISABLE_RELOADER"] = "1"

if "torch.classes" in sys.modules:
    del sys.modules["torch.classes"]

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)

from predictor import final_prediction
from single_sequence import single_sequence
from batch_sequences import batch_sequences

st.set_page_config(
    page_title="iBitter-Stack",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dm = st.session_state.dark_mode

# ── Palette ──────────────────────────────────────────────────────────────────
if dm:
    BG         = "#111827"
    SURFACE    = "#1f2937"
    SURFACE2   = "#374151"
    BORDER     = "#374151"
    TEXT       = "#f3f4f6"
    MUTED      = "#9ca3af"
    ACCENT     = "#f87171"
    LINK       = "#93c5fd"
    TH_BG      = "#374151"
    TH_FG      = "#f3f4f6"
    HOVER      = "#2d3748"
    CITE_BG    = "#0d1117"
    CHIP_BG    = "#374151"
    PRED_BIT_BG = "#3b1c1c"
    PRED_BIT_FG = "#fca5a5"
    PRED_NON_BG = "#14291f"
    PRED_NON_FG = "#6ee7b7"
    HL_ROW     = "#3b1c1c"
else:
    BG         = "#ffffff"
    SURFACE    = "#f8f9fb"
    SURFACE2   = "#eef0f5"
    BORDER     = "#e5e7eb"
    TEXT       = "#111827"
    MUTED      = "#6b7280"
    ACCENT     = "#c0392b"
    LINK       = "#1d6fa5"
    TH_BG      = "#111827"
    TH_FG      = "#ffffff"
    HOVER      = "#f3f4f6"
    CITE_BG    = "#111827"
    CHIP_BG    = "#eef0f5"
    PRED_BIT_BG = "#fef2f2"
    PRED_BIT_FG = "#b91c1c"
    PRED_NON_BG = "#f0fdf4"
    PRED_NON_FG = "#166534"
    HL_ROW     = "#fef2f2"

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"], .stApp {{
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
    background-color: {BG} !important;
    color: {TEXT} !important;
  }}
  #MainMenu, footer, header {{ visibility: hidden; }}

  .block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1080px;
  }}

  /* ── Toggle button ── */
  div[data-testid="stHorizontalBlock"]:has(.dm-toggle) {{
    justify-content: flex-end;
  }}
  .dm-pill {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 999px;
    padding: 5px 14px 5px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    color: {MUTED};
    cursor: pointer;
    user-select: none;
    transition: background 0.2s;
  }}
  .dm-pill:hover {{ background: {SURFACE2}; }}
  .dm-icon {{ font-size: 0.9rem; }}

  /* ── Site header ── */
  .site-header {{
    text-align: center;
    padding: 0.2rem 0 0.8rem;
  }}
  .site-header h1 {{
    font-size: 2rem;
    font-weight: 700;
    color: {TEXT};
    margin: 0 0 0.3rem;
    letter-spacing: -0.02em;
  }}
  .site-header .subtitle {{
    font-size: 0.88rem;
    color: {MUTED};
    margin: 0 0 0.55rem;
    font-weight: 400;
  }}
  .site-header .authors {{
    font-size: 0.76rem;
    color: {MUTED};
    margin: 0 0 0.2rem;
  }}
  .site-header .authors sup {{ font-size: 0.6rem; color: {ACCENT}; }}
  .site-header .affils {{
    font-size: 0.7rem;
    color: {MUTED};
    opacity: 0.75;
    margin: 0 0 0.4rem;
  }}
  .site-header .affils sup {{ font-size: 0.6rem; color: {ACCENT}; }}
  hr.divider {{
    border: none;
    border-top: 1px solid {BORDER};
    margin: 0.5rem 0 0.8rem;
  }}

  /* ── Metric cards ── */
  .metric-row {{
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 1rem;
  }}
  .metric-card {{
    flex: 1 1 120px;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 0.85rem 0.6rem;
    text-align: center;
  }}
  .metric-card .val {{
    font-size: 1.45rem;
    font-weight: 700;
    color: {ACCENT};
    line-height: 1.2;
  }}
  .metric-card .lbl {{
    font-size: 0.7rem;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.2rem;
  }}

  /* ── Info card ── */
  .info-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
    color: {TEXT};
    line-height: 1.65;
  }}
  .info-card h3 {{
    margin: 0 0 0.8rem;
    font-size: 0.88rem;
    font-weight: 700;
    color: {TEXT};
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border-bottom: 2px solid {ACCENT};
    padding-bottom: 0.35rem;
    display: inline-block;
  }}
  .info-card a {{ color: {LINK}; text-decoration: none; }}
  .info-card a:hover {{ text-decoration: underline; }}
  .info-card p {{ color: {TEXT}; margin: 0; }}

  /* ── Tables ── */
  .feat-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.84rem;
  }}
  .feat-table th {{
    background: {TH_BG};
    color: {TH_FG};
    padding: 0.45rem 0.7rem;
    text-align: left;
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.03em;
  }}
  .feat-table td {{
    padding: 0.4rem 0.7rem;
    border-bottom: 1px solid {BORDER};
    color: {TEXT};
  }}
  .feat-table tr:last-child td {{ border-bottom: none; }}
  .feat-table tr:hover td {{ background: {HOVER}; }}
  .hl-row td {{ font-weight: 700 !important; background: {HL_ROW} !important; }}

  /* ── Section heading ── */
  .section-heading {{
    font-size: 0.82rem;
    font-weight: 700;
    color: {MUTED};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 1.4rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}
  .section-heading::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {BORDER};
  }}

  /* ── Step cards ── */
  .step-row {{
    display: flex;
    gap: 0.7rem;
    align-items: flex-start;
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 0.65rem 0.9rem;
    margin-bottom: 0.5rem;
  }}
  .step-num {{
    background: {ACCENT};
    color: #fff;
    border-radius: 50%;
    width: 22px;
    height: 22px;
    min-width: 22px;
    line-height: 22px;
    text-align: center;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 1px;
  }}
  .step-title {{ font-weight: 600; font-size: 0.87rem; color: {TEXT}; display: block; }}
  .step-desc  {{ font-size: 0.8rem; color: {MUTED}; line-height: 1.5; }}

  /* ── Author chips ── */
  .chip-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin: 0.4rem 0 0.6rem;
  }}
  .chip {{
    background: {CHIP_BG};
    border: 1px solid {BORDER};
    border-radius: 999px;
    padding: 0.25rem 0.7rem;
    font-size: 0.8rem;
    color: {TEXT};
    font-weight: 500;
  }}
  .chip sup {{ font-size: 0.6rem; color: {ACCENT}; }}

  /* ── Citation box ── */
  .cite-box {{
    background: {CITE_BG};
    color: #e2e8f0;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    font-family: 'Courier New', monospace;
    font-size: 0.78rem;
    line-height: 1.7;
    white-space: pre-wrap;
    overflow-x: auto;
    margin-top: 0.5rem;
  }}

  /* ── Prediction banners ── */
  .pred-bitter {{
    background: {PRED_BIT_BG};
    border-left: 4px solid {ACCENT};
    border-radius: 6px;
    padding: 0.75rem 1rem;
    color: {PRED_BIT_FG};
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.8rem;
  }}
  .pred-nonbitter {{
    background: {PRED_NON_BG};
    border-left: 4px solid #16a34a;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    color: {PRED_NON_FG};
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.8rem;
  }}

  /* ── Streamlit widget dark overrides ── */
  {"" if not dm else f"""
  .stTextInput input {{
    background: {SURFACE2} !important;
    color: {TEXT} !important;
    border-color: {BORDER} !important;
  }}
  .stButton button {{
    background: {ACCENT} !important;
    color: white !important;
    border: none !important;
  }}
  [data-testid="stDataFrame"] {{
    background: {SURFACE} !important;
  }}
  [data-testid="metric-container"] {{
    background: {SURFACE} !important;
    border-radius: 8px !important;
    border: 1px solid {BORDER} !important;
  }}
  """}
</style>
""", unsafe_allow_html=True)

# ── Dark mode toggle (top-right) ─────────────────────────────────────────────
_, _c2 = st.columns([9, 1])
with _c2:
    icon  = "☀️" if dm else "🌙"
    label = "Light" if dm else "Dark"
    if st.button(f"{icon} {label}", key="dm_toggle",
                 help="Toggle light / dark mode"):
        st.session_state.dark_mode = not dm
        st.rerun()

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="site-header">
  <h1>iBitter-Stack 🧬</h1>
  <p class="subtitle">A Multi-Representation Ensemble Learning Model for Accurate Bitter Peptide Identification</p>
  <p class="authors">
    Sarfraz Ahmad<sup>1</sup> &nbsp;·&nbsp;
    Momina Ahsan<sup>1</sup> &nbsp;·&nbsp;
    Muhammad Nabeel Asim<sup>2</sup> &nbsp;·&nbsp;
    Andreas Dengel<sup>2</sup> &nbsp;·&nbsp;
    Muhammad Imran Malik<sup>1</sup>
  </p>
  <p class="affils">
    <sup>1</sup>&thinsp;NUST, Islamabad, Pakistan &nbsp;&nbsp;
    <sup>2</sup>&thinsp;DFKI, Kaiserslautern, Germany
  </p>
  <hr class="divider">
</div>
""", unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,
    options=["Single Sequence", "Batch Upload", "Algorithm", "About"],
    icons=["file-earmark-text", "file-earmark-spreadsheet", "gear", "info-circle"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0",
            "background-color": SURFACE,
            "border": f"1px solid {BORDER}",
            "border-radius": "10px",
        },
        "icon": {"color": MUTED, "font-size": "0.85rem"},
        "nav-link": {
            "font-size": "0.86rem",
            "text-align": "center",
            "padding": "0.52rem 1rem",
            "color": TEXT,
        },
        "nav-link-selected": {
            "background-color": ACCENT,
            "color": "white",
            "border-radius": "8px",
            "font-weight": "600",
        },
    },
)

# ── Pages ─────────────────────────────────────────────────────────────────────
if selected == "Single Sequence":
    single_sequence(dm)

elif selected == "Batch Upload":
    batch_sequences()

elif selected == "Algorithm":
    st.markdown('<div class="section-heading">Pipeline Overview</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        iBitter-Stack is a two-tier stacking ensemble integrating <strong>seven diverse feature
        representations</strong> with <strong>eight machine-learning classifiers</strong>, generating
        56 base learners. Only models with MCC&nbsp;>&nbsp;0.80 and Accuracy&nbsp;>&nbsp;90% are
        retained. Their soft-probability outputs form an 8-dimensional meta-dataset, which a
        Logistic Regression meta-learner uses for final classification.
    </div>
    """, unsafe_allow_html=True)

    # Centred pipeline image
    left, mid, right = st.columns([1, 6, 1])
    with mid:
        st.image("src/static/final_pipeline.png", width="stretch")
    st.caption("Figure: iBitter-Stack pipeline — dataset curation → feature representation → base learner selection → meta-learning.")

    # Steps
    st.markdown('<div class="section-heading">Step-by-Step Workflow</div>', unsafe_allow_html=True)
    steps = [
        ("Dataset Curation",
         "BTP640 benchmark: 320 bitter + 320 non-bitter peptides. Ambiguous residues (X, B, U, Z) "
         "and 100%-identity duplicates removed. 80:20 split → BTP-CV (512) and BTP-TS (128)."),
        ("Feature Representation",
         "Seven encodings applied independently: ESM-2 (320-d), DPC (400-d), AAE (60-d), "
         "BPNC (200-d), AAI (36-d), GTPC (125-d), CTD (147-d)."),
        ("Base Learner Training",
         "7 features × 8 classifiers (SVM, DT, NB, KNN, LR, RF, AdaBoost, MLP) = 56 models, "
         "each trained with 10-fold CV and grid-search hyperparameter tuning."),
        ("Optimal Learner Selection",
         "Threshold: MCC > 0.80 and Accuracy > 90%. Eight models qualify: "
         "ESM_RF, ESM_SVM, ESM_MLP, ESM_LR, ESM_ADA, CTD_MLP, CTD_SVM, AAI_RF."),
        ("Meta-Dataset Construction",
         "Each selected learner outputs a soft probability per peptide. "
         "The eight scores are concatenated into one 8-d probability vector per sample."),
        ("Meta-Learner",
         "Logistic Regression (L2, max_iter=1500) trained on the meta-dataset via grid search. "
         "Final output: Bitter / Non-Bitter with confidence score."),
    ]
    for i, (title, desc) in enumerate(steps, 1):
        st.markdown(f"""
        <div class="step-row">
          <div class="step-num">{i}</div>
          <div>
            <span class="step-title">{title}</span>
            <span class="step-desc">{desc}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # Feature & base learner tables
    st.markdown('<div class="section-heading">Feature Representations &amp; Selected Base Learners</div>', unsafe_allow_html=True)
    fc, lc = st.columns(2)
    with fc:
        st.markdown(f"""
        <table class="feat-table">
          <thead><tr><th>Feature</th><th>Dim.</th><th>Type</th></tr></thead>
          <tbody>
            <tr><td>ESM-2 (esm2_t6_8M_UR50D)</td><td>320</td><td>PLM / Deep</td></tr>
            <tr><td>Dipeptide Composition (DPC)</td><td>400</td><td>Compositional</td></tr>
            <tr><td>Amino Acid Entropy (AAE)</td><td>60</td><td>Positional</td></tr>
            <tr><td>Binary Profile N/C-term (BPNC)</td><td>200</td><td>Positional</td></tr>
            <tr><td>Amino Acid Index (AAI)</td><td>36</td><td>Physicochemical</td></tr>
            <tr><td>Global Tripeptide Comp. (GTPC)</td><td>125</td><td>Physicochemical</td></tr>
            <tr><td>Comp.-Transition-Dist. (CTD)</td><td>147</td><td>Physicochemical</td></tr>
          </tbody>
        </table>""", unsafe_allow_html=True)
    with lc:
        st.markdown(f"""
        <table class="feat-table">
          <thead><tr><th>Selected Learner</th><th>CV Acc (%)</th><th>CV MCC</th></tr></thead>
          <tbody>
            <tr><td>ESM_SVM</td><td>85.5</td><td>0.71</td></tr>
            <tr><td>ESM_RF</td><td>83.4</td><td>0.67</td></tr>
            <tr><td>ESM_MLP</td><td>83.6</td><td>0.67</td></tr>
            <tr><td>ESM_LR</td><td>83.6</td><td>0.67</td></tr>
            <tr><td>ESM_ADA</td><td>83.0</td><td>0.66</td></tr>
            <tr><td>CTD_MLP</td><td>81.1</td><td>0.62</td></tr>
            <tr><td>CTD_SVM</td><td>83.2</td><td>0.66</td></tr>
            <tr><td>AAI_RF</td><td>78.5</td><td>0.57</td></tr>
          </tbody>
        </table>""", unsafe_allow_html=True)

    # SOTA table
    st.markdown('<div class="section-heading">Comparison with State-of-the-Art (Independent Test Set)</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <table class="feat-table">
      <thead><tr><th>Predictor</th><th>Algorithm</th><th>Acc (%)</th><th>Sn (%)</th><th>Sp (%)</th><th>MCC</th><th>AUROC</th></tr></thead>
      <tbody>
        <tr><td>iBitter-SCM (2020)</td><td>Scoring Card Method</td><td>84.0</td><td>84.0</td><td>84.0</td><td>0.69</td><td>0.90</td></tr>
        <tr><td>BERT4Bitter (2021)</td><td>BERT + Bi-LSTM</td><td>92.2</td><td>93.8</td><td>90.6</td><td>0.84</td><td>0.96</td></tr>
        <tr><td>iBitter-Fuse (2021)</td><td>SVM</td><td>93.0</td><td>94.0</td><td>92.0</td><td>0.86</td><td>0.93</td></tr>
        <tr><td>iBitter-DRLF (2022)</td><td>LightGBM</td><td>94.0</td><td>92.0</td><td>96.9</td><td>0.89</td><td>0.97</td></tr>
        <tr><td>UniDL4BioPep (2023)</td><td>CNN</td><td>93.8</td><td>92.4</td><td>95.2</td><td>0.87</td><td>0.98</td></tr>
        <tr><td>Bitter-RF (2023)</td><td>Random Forest</td><td>94.0</td><td>94.0</td><td>94.0</td><td>0.88</td><td>0.98</td></tr>
        <tr><td>iBitter-GRE (2025)</td><td>Stacking Ensemble</td><td>96.1</td><td>98.4</td><td>93.8</td><td>0.92</td><td>0.97</td></tr>
        <tr class="hl-row"><td>iBitter-Stack (Ours)</td><td>Stacking Ensemble</td><td>96.1</td><td>95.4</td><td>97.2</td><td>0.92</td><td>0.98</td></tr>
      </tbody>
    </table>""", unsafe_allow_html=True)
    st.caption("Sn = Sensitivity · Sp = Specificity · MCC = Matthews Correlation Coefficient · AUROC = Area Under ROC Curve")

# ── About ─────────────────────────────────────────────────────────────────────
elif selected == "About":
    # Metrics
    st.markdown('<div class="section-heading">Model Performance — Independent Test Set</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="metric-row">
      <div class="metric-card"><div class="val">96.1%</div><div class="lbl">Accuracy</div></div>
      <div class="metric-card"><div class="val">0.922</div><div class="lbl">MCC</div></div>
      <div class="metric-card"><div class="val">0.981</div><div class="lbl">AUROC</div></div>
      <div class="metric-card"><div class="val">95.4%</div><div class="lbl">Sensitivity</div></div>
      <div class="metric-card"><div class="val">97.2%</div><div class="lbl">Specificity</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Abstract
    st.markdown('<div class="section-heading">Abstract</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        The identification of bitter peptides is crucial in food science, drug discovery, and
        biochemical research. These peptides contribute to the undesirable taste of hydrolyzed
        proteins and play key roles in physiological and pharmacological processes. With the rapid
        expansion of peptide sequence databases, the demand for efficient computational approaches
        to distinguish bitter from non-bitter peptides has become increasingly significant.
        <br><br>
        We propose a novel <strong>stacking-based ensemble learning framework</strong> that integrates
        diverse sequence-based feature representations with a broad set of machine learning classifiers.
        The first stacking layer comprises multiple base classifiers, each trained on a distinct feature
        encoding scheme; the second layer employs Logistic Regression to refine predictions using an
        eight-dimensional probability vector. Extensive evaluations demonstrate that our model
        significantly outperforms existing predictive methods, achieving <strong>96.09% accuracy</strong>
        and an <strong>MCC of 0.9220</strong> on the independent test set.
    </div>
    """, unsafe_allow_html=True)

    # Dataset
    st.markdown('<div class="section-heading">Dataset</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <h3>BTP640 Benchmark</h3>
        <table class="feat-table" style="width:auto; min-width:380px; margin-top:0.6rem;">
          <thead><tr><th>Split</th><th>Bitter</th><th>Non-Bitter</th><th>Total</th></tr></thead>
          <tbody>
            <tr><td>Training (BTP-CV)</td><td>256</td><td>256</td><td>512</td></tr>
            <tr><td>Independent Test (BTP-TS)</td><td>64</td><td>64</td><td>128</td></tr>
            <tr><td><strong>Total</strong></td><td><strong>320</strong></td><td><strong>320</strong></td><td><strong>640</strong></td></tr>
          </tbody>
        </table>
        <p style="margin-top:0.8rem; font-size:0.85rem; color:{MUTED};">
            Bitter peptides sourced from peer-reviewed experimental studies.
            Non-bitter peptides randomly sampled from the
            <a href="http://www.uwm.edu.pl/biochemia/index.php/pl/biopep" target="_blank">BIOPEP database</a>.
            An 80%-identity filtered experiment confirmed robustness (Acc: 95.3%, MCC: 0.91, AUROC: 0.98).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Authors & affiliations
    st.markdown('<div class="section-heading">Authors &amp; Affiliations</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <div class="chip-row">
            <span class="chip">Sarfraz Ahmad<sup> 1 ✉</sup></span>
            <span class="chip">Momina Ahsan<sup> 1</sup></span>
            <span class="chip">Muhammad Nabeel Asim<sup> 2</sup></span>
            <span class="chip">Andreas Dengel<sup> 2</sup></span>
            <span class="chip">Muhammad Imran Malik<sup> 1</sup></span>
        </div>
        <p style="font-size:0.82rem; color:{MUTED}; line-height:1.9; margin:0.2rem 0 0;">
            <sup>1</sup> National University of Sciences and Technology (NUST), H-12, Islamabad, Pakistan<br>
            <sup>2</sup> German Research Center for Artificial Intelligence (DFKI), Kaiserslautern, 67663, Germany<br>
            <sup>✉</sup> Corresponding:
            <a href="mailto:sarfaraz_076@outlook.com">sarfaraz_076@outlook.com</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Publication & links
    st.markdown('<div class="section-heading">Publication &amp; Resources</div>', unsafe_allow_html=True)
    pc, lc = st.columns([3, 2])
    with pc:
        st.markdown(f"""
        <div class="info-card" style="height:100%;">
            <h3>Journal of Molecular Biology</h3>
            <p style="font-size:0.86rem; line-height:2.0;">
                <strong>Volume:</strong> 437, Issue 24 · Article 169448<br>
                <strong>Year:</strong> 2025 &nbsp;·&nbsp; <strong>Publisher:</strong> Elsevier<br>
                <strong>DOI:</strong>
                <a href="https://doi.org/10.1016/j.jmb.2025.169448" target="_blank">
                10.1016/j.jmb.2025.169448</a>
            </p>
        </div>
        """, unsafe_allow_html=True)
    with lc:
        st.markdown(f"""
        <div class="info-card" style="height:100%;">
            <h3>Links</h3>
            <p style="font-size:0.86rem; line-height:2.3;">
                🌐 <a href="https://ibitter-stack-webserver.streamlit.app" target="_blank"><strong>Web Server</strong></a><br>
                💻 <a href="https://github.com/SarfrazAhmad307/iBitter-Stack" target="_blank"><strong>GitHub</strong></a><br>
                📄 <a href="https://doi.org/10.1016/j.jmb.2025.169448" target="_blank"><strong>ScienceDirect</strong></a><br>
                📦 <a href="https://arxiv.org/abs/2505.15730" target="_blank"><strong>arXiv Preprint</strong></a>
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Citation — combined BibTeX (covers both paper record & Google Scholar record)
    st.markdown('<div class="section-heading">Citation</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-card">
        <h3>BibTeX</h3>
        <div class="cite-box">@article{{ahmad2025ibitter,
  title     = {{iBitter-Stack: A multi-representation ensemble learning model
               for accurate bitter peptide identification}},
  author    = {{Ahmad, Sarfraz and Ahsan, Momina and Asim, Muhammad Nabeel
               and Dengel, Andreas and Malik, Muhammad Imran}},
  journal   = {{Journal of Molecular Biology}},
  volume    = {{437}},
  number    = {{24}},
  pages     = {{169448}},
  year      = {{2025}},
  publisher = {{Elsevier}},
  doi       = {{10.1016/j.jmb.2025.169448}},
  url       = {{https://www.sciencedirect.com/science/article/pii/S0022283625005145}}
}}</div>
        <p style="font-size:0.82rem; color:{MUTED}; margin-top:0.9rem; line-height:1.6;">
            <strong>APA:</strong> Ahmad, S., Ahsan, M., Asim, M. N., Dengel, A., &amp; Malik, M. I. (2025).
            iBitter-Stack: A multi-representation ensemble learning model for accurate bitter peptide identification.
            <em>Journal of Molecular Biology</em>, 437(24), 169448.
            <a href="https://doi.org/10.1016/j.jmb.2025.169448" target="_blank">https://doi.org/10.1016/j.jmb.2025.169448</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="text-align:center; font-size:0.74rem; color:{MUTED}; margin-top:1.5rem;">
        iBitter-Stack is provided for academic and research purposes only.
        Computational predictions should be validated experimentally.
    </p>
    """, unsafe_allow_html=True)
