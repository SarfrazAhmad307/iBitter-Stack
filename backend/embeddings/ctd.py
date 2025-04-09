import math

# Define amino acid groups for each physicochemical property
group1 = {
    "hydrophobicity_PRAM900101": "RKEDQN",
    "normwaalsvolume": "GASTPDC",
    "polarity": "LIFWCMVY",
    "polarizability": "GASDT",
    "charge": "KR",
    "secondarystruct": "EALMQKRH",
    "solventaccess": "ALFCGIVW",
}
group2 = {
    "hydrophobicity_PRAM900101": "GASTPHY",
    "normwaalsvolume": "NVEQIL",
    "polarity": "PATGS",
    "polarizability": "CPNVEQIL",
    "charge": "ANCQGHILMFPSTWYV",
    "secondarystruct": "VIYCWFT",
    "solventaccess": "RKQEND",
}
group3 = {
    "hydrophobicity_PRAM900101": "CLVIMFW",
    "normwaalsvolume": "MHKFRYW",
    "polarity": "HQRKNED",
    "polarizability": "KMHFRYW",
    "charge": "DE",
    "secondarystruct": "GNPSD",
    "solventaccess": "MSPTHY",
}
groups = [group1, group2, group3]

propertys = (
    "hydrophobicity_PRAM900101",
    "normwaalsvolume",
    "polarity",
    "polarizability",
    "charge",
    "secondarystruct",
    "solventaccess",
)


def Count_C(sequence1, sequence2):
    return sum(sequence2.count(aa) for aa in sequence1)


def Count_D(aaSet, sequence):
    number = sum(1 for aa in sequence if aa in aaSet)
    cutoffNums = [
        1,
        math.floor(0.25 * number),
        math.floor(0.5 * number),
        math.floor(0.75 * number),
        number,
    ]
    cutoffNums = [max(1, i) for i in cutoffNums]
    code = []
    for cutoff in cutoffNums:
        myCount = 0
        for i, aa in enumerate(sequence):
            if aa in aaSet:
                myCount += 1
                if myCount == cutoff:
                    code.append((i + 1) / len(sequence))
                    break
        if myCount == 0:
            code.append(0)
    return code


def compute_ctd(seq):
    encodings = []
    code, code2, CTDD1, CTDD2, CTDD3 = [], [], [], [], []

    aaPair = [seq[i : i + 2] for i in range(len(seq) - 1)]

    for p in propertys:
        # Composition
        c1 = Count_C(group1[p], seq) / len(seq)
        c2 = Count_C(group2[p], seq) / len(seq)
        c3 = 1 - c1 - c2
        code += [c1, c2, c3]

        # Transition
        c1221 = c1331 = c2332 = 0
        for pair in aaPair:
            if (pair[0] in group1[p] and pair[1] in group2[p]) or (
                pair[0] in group2[p] and pair[1] in group1[p]
            ):
                c1221 += 1
            elif (pair[0] in group1[p] and pair[1] in group3[p]) or (
                pair[0] in group3[p] and pair[1] in group1[p]
            ):
                c1331 += 1
            elif (pair[0] in group2[p] and pair[1] in group3[p]) or (
                pair[0] in group3[p] and pair[1] in group2[p]
            ):
                c2332 += 1
        code2 += [c1221 / len(aaPair), c1331 / len(aaPair), c2332 / len(aaPair)]

        # Distribution
        CTDD1 += [val / len(seq) for val in Count_D(group1[p], seq)]
        CTDD2 += [val / len(seq) for val in Count_D(group2[p], seq)]
        CTDD3 += [val / len(seq) for val in Count_D(group3[p], seq)]

    encodings.append(code + code2 + CTDD1 + CTDD2 + CTDD3)
    return encodings[0]  # return feature list for a single sequence
