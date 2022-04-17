from pathlib import Path
import argparse

from vpgenerator import dictionarytools

parser = argparse.ArgumentParser(description="Script to merge two dictionaries and export the result.")
parser.add_argument("dicoA", type=Path, help="Path to dictionary A")
parser.add_argument("dicoB", type=Path, help="Path to dictionary B")
parser.add_argument("--output", "-o", type=Path, help="Path to output dictionary. If not set, the result will be exported to dicoA", default=None)
parser.add_argument("--force", "-f", action='store_true', help="Force B value in output dico if conflicts detected.")

args = parser.parse_args()

if args.output is None:
    dictionarytools.merge_dico(args.dicoA, args.dicoB, args.dicoA, args.force)
else:
    dictionarytools.merge_dico(args.dicoA, args.dicoB, args.output, args.force)