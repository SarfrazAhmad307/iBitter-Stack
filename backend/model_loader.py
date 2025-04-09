import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

BASE_MODEL_NAMES = [
    "AAI_RF.pkl",
    "CTD_MLP.pkl",
    "CTD_SVM.pkl",
    "ESM_LR.pkl",
    "ESM_ADA.pkl",
    "ESM_MLP.pkl",
    "ESM_RF.pkl",
    "ESM_SVM.pkl",
]

BASE_MODELS = {
    name.split(".")[0]: joblib.load(os.path.join(MODEL_DIR, name))
    for name in BASE_MODEL_NAMES
}
META_MODEL = joblib.load(os.path.join(MODEL_DIR, "LR.pkl"))
