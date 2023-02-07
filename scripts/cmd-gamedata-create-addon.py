from pathlib import Path
import argparse


from gamedata import cmdgamedata

parser = argparse.ArgumentParser(description="Script to explore wow game data and save the file in the repository db")
parser.add_argument("--lang", "-l", type=str, help="Set the dictionnary lang (e.g. en, fr, de, etc)", required=True)
parser.add_argument("--id", "-id", type=int, help="Instance id", required=False, default=0)
parser.add_argument("--gamedatadbpath", "-gdbp", type=Path, help="Path to import gamedata db (dir)", required=True)
parser.add_argument("--addondbpath", "-adbp", type=Path, help="Path to export addon(s) (dir)", required=True)

args = parser.parse_args()


cmdgamedata.create_addon(args.id, args.lang, args.gamedatadbpath, args.addondbpath)