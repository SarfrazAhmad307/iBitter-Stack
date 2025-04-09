import os
from pathlib import Path

# Define the base path as the project root
BASE_DIR = Path(__file__).resolve().parent.parent
AAI_INDEX_1_PATH = BASE_DIR / "aai_helpers" / "AAindex_1.txt"
AAI_INDEX_2_PATH = BASE_DIR / "aai_helpers" / "AAindex_2.txt"

# Standard 20 amino acids
letters = list("ACDEFGHIKLMNPQRSTVWY")


def AAI_1(fastas):
    encodings = []

    with open(AAI_INDEX_1_PATH) as fileAAindex1, open(AAI_INDEX_2_PATH) as fileAAindex2:
        records1 = fileAAindex1.readlines()[1:]
        records2 = fileAAindex2.readlines()[1:]

    AAindex1 = [line.strip().split()[1:] for line in records1 if line.strip()]
    AAindex2 = [line.strip().split()[1:] for line in records2 if line.strip()]

    # Mapping: amino acid → index
    index = {aa: i for i, aa in enumerate(letters)}

    fastas_len = len(fastas)
    for aa_vec in AAindex1:
        total = sum(float(aa_vec[index[fastas[j]]]) for j in range(fastas_len))
        encodings.append(total / fastas_len)
    for aa_vec in AAindex2:
        total = sum(float(aa_vec[index[fastas[j]]]) for j in range(fastas_len))
        encodings.append(total)

    return encodings


def compute_aai(seq):
    """
    Full AAI features = Global + N-terminal 5 + C-terminal 5 regions
    """
    seq = seq.upper()
    if any(aa not in letters for aa in seq):
        raise ValueError(f"Sequence contains invalid amino acids: {seq}")

    encodings_full = AAI_1(seq)
    encodings_NT5 = AAI_1(seq[:5])
    encodings_CT5 = AAI_1(seq[-5:])

    return encodings_full + encodings_NT5 + encodings_CT5
