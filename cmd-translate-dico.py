from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dico", type=Path, help="Path to dictionary A to update")
parser.add_argument("langsrc", type=str, help="Lang src in dictionary")
parser.add_argument("langto", type=str, help="Lang dest in dictionary")
parser.add_argument("--output", "-o", type=Path, help="Path to output dico", default=None)
parser.add_argument("--force", "-f", action='store_true', help="Force B value in output dico if conflicts detected.")

args = parser.parse_args()

if args.output is None:
    libcmd.translate(args.dico, args.langsrc, args.langto, args.dico, args.force)
else:
    libcmd.translate(args.dico, args.langsrc, args.langto, args.output, args.force)