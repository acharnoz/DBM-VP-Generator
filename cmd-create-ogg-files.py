from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("dico", type=Path, help="Path to dictionary read")
parser.add_argument("lang", type=str, help="Lang src in dictionary")
parser.add_argument("outputdir", type=Path, help="Path to save ogg files")
parser.add_argument("--key", "-k", type=str, help="Path to output dico", default=None)
parser.add_argument("--domain", "-d", type=str, help="Path to output dico", default="com")

args = parser.parse_args()

if args.key is None:
    libcmd.generate_ogg_files_with_gtts(args.dico, args.lang, args.domain, args.outputdir)
else:
    libcmd.generate_ogg_file_with_gtts(args.dico, args.lang, args.domain, args.key, args.outputdir)