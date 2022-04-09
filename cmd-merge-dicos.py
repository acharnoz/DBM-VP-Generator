from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dicoA", type=Path, help="Path to dictionary A")
parser.add_argument("dicoB", type=Path, help="Path to dictionary B")
parser.add_argument("--output", "-o", type=Path, help="Path to output dico", default=None)
parser.add_argument("--force", "-f", action='store_true', help="Force B value in output dico if conflicts detected.")

args = parser.parse_args()

if args.output is None:
    libcmd.merge_dico(args.dicoA, args.dicoB, args.dicoA, args.force)
else:
    libcmd.merge_dico(args.dicoA, args.dicoB, args.output, args.force)