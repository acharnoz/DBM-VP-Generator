from pathlib import Path
import argparse

from vpgenerator import dictionarytools

parser = argparse.ArgumentParser(description="Script to create an empty dictionary from .ogg files included in an addon folder")
parser.add_argument("addondir", type=Path, help="Path to addon folder to browse .ogg files (e.g. VPVEM addon)")
parser.add_argument("--lang", "-l", type=str, help="Set the dictionnary lang (e.g. en, fr, de, etc)", required=True)
parser.add_argument("--name", "-n", type=str, help="Name of the new dictionary (e.g. VP Male English)", required=True)
parser.add_argument("--dicopath", "-o", type=Path, help="Path to export new dictionary in .json format(e.g. dico.json)", required=True)

args = parser.parse_args()

dictionarytools.create_dico(args.addondir, args.lang, args.name, args.dicopath)