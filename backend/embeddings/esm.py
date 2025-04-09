import torch
import esm
import joblib
import numpy as np
import os
from pathlib import Path

# Load ESM model once
esm_model, alphabet = esm.pretrained.esm2_t6_8M_UR50D()
batch_converter = alphabet.get_batch_converter()
esm_model.eval()

# Load fitted MinMaxScaler
scaler_path = Path(__file__).resolve().parent.parent / "saved_models" / "esm_scaler.pkl"
scaler = joblib.load(scaler_path)


def compute_esm(seq: str):
    """
    Compute normalized ESM embedding for a single sequence.
    """
    formatted_input = [("seq1", seq)]
    batch_labels, batch_strs, batch_tokens = batch_converter(formatted_input)
    batch_lens = (batch_tokens != alphabet.padding_idx).sum(1)

    with torch.no_grad():
        results = esm_model(batch_tokens, repr_layers=[6], return_contacts=False)

    token_representations = results["representations"][6]
    rep = token_representations[0, 1 : batch_lens[0] - 1].mean(0)
    rep_np = rep.numpy().reshape(1, -1)  # reshape for scaler

    rep_scaled = scaler.transform(rep_np)  # normalize
    return rep_scaled[0].tolist()
