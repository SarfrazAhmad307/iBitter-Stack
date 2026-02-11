import joblib
import os
import sys
import pickle

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


def safe_load_model(filepath):
    """Load a model with better error handling for pickle version issues."""
    try:
        # Try standard joblib load
        return joblib.load(filepath)
    except (KeyError, ValueError, pickle.UnpicklingError) as e:
        print(f"Warning: Failed to load {filepath} with error: {e}")
        print(f"Python version: {sys.version}")

        # Try alternative loading methods
        attempts = [
            lambda: pickle.load(open(filepath, "rb"), encoding="latin1"),
            lambda: pickle.load(open(filepath, "rb"), fix_imports=True),
            lambda: pickle.load(open(filepath, "rb")),
        ]

        for i, attempt in enumerate(attempts):
            try:
                model = attempt()
                print(f"✓ Successfully loaded {filepath} using method {i+1}")
                return model
            except Exception as e2:
                if i == len(attempts) - 1:
                    # Last attempt failed
                    raise Exception(
                        f"Cannot load model from {filepath}. "
                        f"Pickle version incompatibility detected (KeyError: 118). "
                        f"Current Python: {sys.version_info.major}.{sys.version_info.minor}. "
                        f"The models were likely created with Python 3.12+. "
                        f"Please either:\n"
                        f"  1. Use Python 3.12+ to run this application, or\n"
                        f"  2. Re-train and save the models with Python {sys.version_info.major}.{sys.version_info.minor}"
                    )
                continue


BASE_MODELS = {
    name.split(".")[0]: safe_load_model(os.path.join(MODEL_DIR, name))
    for name in BASE_MODEL_NAMES
}
META_MODEL = safe_load_model(os.path.join(MODEL_DIR, "LR.pkl"))
