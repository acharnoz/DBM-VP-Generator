from pathlib import Path
import argparse


from gamedata import cmdgamedata

parser = argparse.ArgumentParser(description="Script to explore wow game data and save the file in the repository db")
parser.add_argument("--lang", "-l", type=str, help="Set the dictionnary lang (e.g. en, fr, de, etc)", required=True)
parser.add_argument("--gamedatadbpath", "-gdbp", type=Path, help="Path to import gamedata db (dir)", required=True)
parser.add_argument("--addondbpath", "-adbp", type=Path, help="Path to export addon(s) (dir)", required=True)

args = parser.parse_args()

         
# "Dragonflight",
DF = [1201,1196,1204,1199,1202,1203,1198,1197,1205,1200]
DF_s1 = [721, 800, 537, 313]
all = []
all.extend(DF)
all.extend(DF_s1)

isntance_keys=[]
for id in all:
    isntance_keys.append(str(id))

cmdgamedata.create_addon_v2(isntance_keys, args.lang, args.gamedatadbpath, args.addondbpath)

