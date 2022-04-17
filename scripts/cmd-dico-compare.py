from pathlib import Path
import argparse

from vpgenerator import dictionarytools


parser = argparse.ArgumentParser(description="Script to compare two dictionaries and print result.")
parser.add_argument("dicoA", type=Path, help="Path to dictionary A")
parser.add_argument("dicoB", type=Path, help="Path to dictionary B")

args = parser.parse_args()

dictionarytools.compare_dicos(args.dicoA, args.dicoB)