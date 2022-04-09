from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dicoIn", type=Path, help="Path to input dico")
parser.add_argument("lang", type=str, help="Added lang (e.g. en, fr, de, etc")
parser.add_argument("--output", "-o", type=Path, help="Path to output dico", default=None)

args = parser.parse_args()

if args.output is None:
    libcmd.remove_lang_dico(args.dicoIn, args.dicoIn, args.lang)
else:
    libcmd.remove_lang_dico(args.dicoIn, args.output, args.lang)