#!/usr/bin/env python3
"""Check the pickle protocol version of model files."""

import os
import struct

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")


def check_pickle_protocol(filepath):
    """Read the pickle protocol from a file."""
    try:
        with open(filepath, "rb") as f:
            # Read first few bytes
            header = f.read(20)

            print(f"\n{os.path.basename(filepath)}:")
            print(f"  First 20 bytes (hex): {header.hex()}")
            print(f"  First 20 bytes (repr): {repr(header)}")

            # Pickle files start with specific opcodes
            if len(header) >= 2:
                first_byte = header[0]
                second_byte = header[1]

                # Protocol 0-2 start with specific opcodes
                if first_byte == 0x80:  # PROTO opcode
                    protocol = second_byte
                    print(f"  ✓ Pickle protocol: {protocol}")

                    if protocol >= 5:
                        print(f"    ⚠ Protocol {protocol} requires Python 3.8+")
                    elif protocol == 4:
                        print(f"    ✓ Protocol {protocol} compatible with Python 3.4+")
                else:
                    print(
                        f"  ? Unusual first byte: {first_byte} (might be protocol 0-2 or corrupted)"
                    )

    except Exception as e:
        print(f"\n{os.path.basename(filepath)}: Error - {e}")


if __name__ == "__main__":
    import sys

    print(f"Python version: {sys.version}")
    print(f"Model directory: {MODEL_DIR}")

    models = [
        "AAI_RF.pkl",
        "CTD_MLP.pkl",
        "ESM_LR.pkl",
        "LR.pkl",
    ]

    for model in models:
        filepath = os.path.join(MODEL_DIR, model)
        if os.path.exists(filepath):
            check_pickle_protocol(filepath)
        else:
            print(f"\n{model}: File not found")
