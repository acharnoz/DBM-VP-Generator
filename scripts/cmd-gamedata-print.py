from pathlib import Path
import argparse


from gamedata import cmdgamedata

parser = argparse.ArgumentParser(description="Script to explore wow game data and save the file in the repository db")
parser.add_argument("--lang", "-l", type=str, help="Set the dictionnary lang (e.g. en, fr, de, etc)", required=True)
parser.add_argument("--id", "-id", type=int, help="Id Expansion", required=False, default=0)
#parser.add_argument("--allid", "-aid", type=bool, help="All Expansions", required=False)
parser.add_argument("--dbpath", "-dbp", type=Path, help="Path to export game data db", required=True)

args = parser.parse_args()

# if args.allid:
#     cmdgamedata.explore([68,70,72,73,74,124,395,396,499,503], args.lang, args.dbpath)
# else:
#     cmdgamedata.explore([args.id], args.lang, args.dbpath)

#cmdgamedata.print_random_encounter(args.lang, args.dbpath)
cmdgamedata.print_random_instance(args.lang, args.dbpath)