from pathlib import Path
import argparse

from vpgenerator import audiofilestools
from vpgenerator import gttsengine


parser = argparse.ArgumentParser(description="Script to create an ogg file from a text")

parser.add_argument("text", type=str, help="Text to convert (eg 'Run away !')")
parser.add_argument("--output", "-o", type=Path, help="Output ogg filepath (eg my_sound.ogg)", required=True)
parser.add_argument("--engine", "-e", type=str, help="Name of the AI audio engine to use", default=gttsengine.GTTS_ENGINE)
parser.add_argument("--config", "-c", type=Path, help="Path to a specific audio config", default=None)


# Parse arguments of the command line        
args = parser.parse_args()

audiofilestools.create_voice(args.text, args.engine, args.config, args.output)