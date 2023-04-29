import json
import random

from gamedata import wowgamedata
from gamedata import addon
from gamedata import multiaddon
from gamedata import structures
from pathlib import Path


def load_game_data(lang: str, gamedatadbpath: Path) -> wowgamedata.WowGameData:

    wgd = wowgamedata.WowGameData()
    wgd.lang = lang

    # Load if file db exist
    file_db_path = wgd.get_db_file_path(gamedatadbpath)
    if file_db_path.exists():
        print(f"File {file_db_path} loading...")
        wgd.load(gamedatadbpath)
        print(f"File loaded.")

    return wgd


def explore(journal_expansion_ids, lang: str, gamedatadbpath: Path):

    wgd = load_game_data(lang, gamedatadbpath)

    # Explore
    print(f"Game data exploring...")
    wgd.configure_api()
    wgd.explore_expansions(journal_expansion_ids)
    print(f"Game data explored.")

    # Save result
    print(f"File saving...")
    wgd.save(gamedatadbpath)
    print(f"File saved.")


def print_random_encounter(lang: str, gamedatadbpath: Path):

    wgd = load_game_data(lang, gamedatadbpath)

    # Select an encounter
    rand_key = random.choice(list(wgd.journal_encounters.keys()))
    print(wgd.journal_encounters[rand_key].to_string())


def print_random_instance(lang: str, gamedatadbpath: Path):

    wgd = load_game_data(lang, gamedatadbpath)

    # Select an encounter
    rand_key = random.choice(list(wgd.journal_instances.keys()))
    print(wgd.journal_instances[rand_key].to_string())


def print_instance_by_extension(lang: str, gamedatadbpath: Path):

    wgd = load_game_data(lang, gamedatadbpath)

    for expansion_id, expension in wgd.journal_expansions.items():
        name = expension.data["name"]
        print(f"{expansion_id}:{name}")

        print("--Dungeon")
        for dungeon_id in expension.get_dungeons_ids():
            ji = wgd.journal_instances[str(dungeon_id)]    
            print(f"----{dungeon_id}:{ji.get_name()}")

        print("--Raid")
        for raid_id in expension.get_raids_ids():
            ji = wgd.journal_instances[str(raid_id)]    
            print(f"----{raid_id}:{ji.get_name()}")

def create_addon(id: int, lang: str, gamedatadbpath: Path, addondbpath: Path):

   addonmger = addon.AddonManager()
   wgd = load_game_data(lang, gamedatadbpath)
   addonmger.set_param(str(id), wgd, addondbpath)

   addonmger.create_addon()


def create_addon_from_ids(ids, lang: str, gamedatadbpath: Path, addondbpath: Path, addon_foldername:str, addon_title:str, generate_sounds: bool= False):
   addonmger = multiaddon.MultiAddonManager()
   wgd = load_game_data(lang, gamedatadbpath)
   addonmger.set_param(addon_foldername,
                       addon_title, ids, wgd, addondbpath)

   addonmger.create_addon(generate_sounds)
