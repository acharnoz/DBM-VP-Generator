from pathlib import Path
import argparse

from vpgenerator import audiofilestools
from vpgenerator import gttsengine


parser = argparse.ArgumentParser(description="Script to update a voice pack from dictionary differences")
parser.add_argument("dico", type=Path, help="Path to the dictionary")
parser.add_argument("olddico", type=Path, help="Path to the old dictionary")
parser.add_argument("--output", "-o", type=Path, help="Output directory to save ogg files (eg oggfiles/)", required=True)
parser.add_argument("--engine", "-e", type=str, help="Name of the AI audio engine to use", default=gttsengine.GTTS_ENGINE)
parser.add_argument("--config", "-c", type=Path, help="Path to a specific audio config", default=None)


# Parse arguments of the command line        
args = parser.parse_args()

audiofilestools.update_voicepack(args.dico, args.olddico, args.engine, args.config, args.output)