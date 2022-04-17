from pathlib import Path
import argparse

from vpgenerator import translationtools

parser = argparse.ArgumentParser(description="Script to translate a dictionary and export the result")
parser.add_argument("dico", type=Path, help="Path to dictionary to translate")
parser.add_argument("--lang", "-l", type=str, help="Lang for the new dictionary")
parser.add_argument("--output", "-o", type=Path, help="Path to export the new dictionary.", required=True)

args = parser.parse_args()

translationtools.translate(args.dico, args.lang, args.output)