from pathlib import Path
import argparse

import libcmd

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("addondir", type=Path, help="Path to addon directory to browse .ogg files (e.g. )")
parser.add_argument("lang", type=str, help="Initialization lang (e.g. en, fr, de, etc")
parser.add_argument("dico", type=Path, help="Path to export new dictionary (e.g. dico.json")
parser.add_argument("--usefilename", "-uf", action='store_true', help="By default txt dictionary is configured with TODO, with this option the text is set with the filename")

args = parser.parse_args()

libcmd.create_dico(args.addondir, args.lang, args.dico, args.usefilename)