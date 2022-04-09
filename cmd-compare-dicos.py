from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dicoA", type=Path, help="Path to dictionary A")
parser.add_argument("dicoB", type=Path, help="Path to dictionary B")


args = parser.parse_args()

libcmd.compare_dicos(args.dicoA, args.dicoB)