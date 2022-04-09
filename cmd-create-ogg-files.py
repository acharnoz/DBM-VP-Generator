from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dico", type=Path, help="Path to dictionary read")
parser.add_argument("lang", type=str, help="Lang src in dictionary")
parser.add_argument("outputdir", type=Path, help="Path to save ogg files")
parser.add_argument("--key", "-k", type=str, help="Path to output dico", default=None)

args = parser.parse_args()

if args.key is None:
    libcmd.generate_ogg_files(args.dico, args.lang, args.outputdir)
else:
    libcmd.generate_ogg_file(args.dico, args.lang, args.key, args.outputdir)