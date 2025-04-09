from model_loader import BASE_MODELS, META_MODEL
from embeddings import esm, aai, ctd

MODEL_TO_EMBEDDING = {
    "AAI_RF": "AAI",
    "CTD_MLP": "CTD",
    "CTD_SVM": "CTD",
    "ESM_ADA": "ESM",
    "ESM_LR": "ESM",
    "ESM_MLP": "ESM",
    "ESM_RF": "ESM",
    "ESM_SVM": "ESM",
}


def extract_features(sequence, model_type):
    emb_type = MODEL_TO_EMBEDDING[model_type]
    if emb_type == "AAI":
        return aai.compute_aai(sequence)
    elif emb_type == "CTD":
        return ctd.compute_ctd(sequence)
    elif emb_type == "ESM":
        return esm.compute_esm(sequence)
    else:
        raise ValueError("Unknown embedding type")


def get_model_predictions(sequence):
    base_probs = []
    for model_name, model in BASE_MODELS.items():
        features = extract_features(sequence, model_name)
        prob = model.predict_proba([features])[0][1]
        base_probs.append(prob)
    return base_probs


def final_prediction(sequence):
    base_probs = get_model_predictions(sequence)
    result = META_MODEL.predict([base_probs])[0]
    conf = META_MODEL.predict_proba([base_probs])[0][1]
    return {
        "base_probs": dict(zip(BASE_MODELS.keys(), base_probs)),
        "final_prediction": "Bitter" if result == 1 else "Non-Bitter",
        "confidence": round(conf, 4),
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) != 2:
        print("Usage: python predictor.py <sequence>")
        sys.exit(1)

    sequence = sys.argv[1]
    result = final_prediction(sequence)

    print(json.dumps(result, indent=4))
