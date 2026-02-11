#!/usr/bin/env python3
"""
Utility script to fix pickle compatibility issues.
This script attempts to load models and re-save them with protocol 4,
which is compatible with Python 3.4+.
"""

import os
import sys
import pickle
import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")

MODEL_FILES = [
    "AAI_RF.pkl",
    "CTD_MLP.pkl",
    "CTD_SVM.pkl",
    "ESM_LR.pkl",
    "ESM_ADA.pkl",
    "ESM_MLP.pkl",
    "ESM_RF.pkl",
    "ESM_SVM.pkl",
    "LR.pkl",
    "esm_scaler.pkl",
]


def convert_pickle(filepath):
    """Try to load and re-save a pickle file with compatible protocol."""
    print(f"Processing: {filepath}")

    # Backup original
    backup_path = filepath + ".backup"
    if not os.path.exists(backup_path):
        os.rename(filepath, backup_path)
        print(f"  Created backup: {backup_path}")
    else:
        filepath_to_load = backup_path
        print(f"  Using existing backup: {backup_path}")

    model = None

    # Try different loading methods
    loading_methods = [
        ("standard pickle", lambda: pickle.load(open(backup_path, "rb"))),
        (
            "pickle with latin1",
            lambda: pickle.load(open(backup_path, "rb"), encoding="latin1"),
        ),
        (
            "pickle with bytes",
            lambda: pickle.load(open(backup_path, "rb"), encoding="bytes"),
        ),
    ]

    for method_name, method in loading_methods:
        try:
            model = method()
            print(f"  ✓ Loaded successfully with {method_name}")
            break
        except Exception as e:
            print(f"  ✗ Failed with {method_name}: {e}")
            continue

    if model is None:
        print(f"  ✗ Could not load {filepath} with any method")
        return False

    # Re-save with protocol 4 (compatible with Python 3.4+)
    try:
        joblib.dump(model, filepath, protocol=4)
        print(f"  ✓ Re-saved with protocol 4")
        return True
    except Exception as e:
        print(f"  ✗ Failed to save: {e}")
        # Restore backup
        if os.path.exists(backup_path):
            os.rename(backup_path, filepath)
        return False


def main():
    print(f"Python version: {sys.version}")
    print(f"Model directory: {MODEL_DIR}\n")

    if not os.path.exists(MODEL_DIR):
        print(f"Error: Model directory not found: {MODEL_DIR}")
        return

    success_count = 0
    for model_file in MODEL_FILES:
        filepath = os.path.join(MODEL_DIR, model_file)
        if not os.path.exists(filepath) and not os.path.exists(filepath + ".backup"):
            print(f"Skipping {model_file} (not found)")
            continue

        if convert_pickle(filepath):
            success_count += 1
        print()

    print(
        f"Conversion complete: {success_count}/{len(MODEL_FILES)} models converted successfully"
    )
    print("\nTo restore original files, rename the .backup files back to .pkl")


if __name__ == "__main__":
    main()
