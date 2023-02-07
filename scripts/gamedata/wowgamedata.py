import json
import random

from gamedata import wowapi
from gamedata import structures
from pathlib import Path


def save(data, path:Path) -> None:
    Path.mkdir(path.parent, parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False,
                  indent=4, separators=(',', ': '))


def load(path:Path):
    with open(path, encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data
    

class WowGameData:

    def __init__(self):
        self.lang = "en"
        self.journal_expansions = {}
        self.journal_instances = {}
        self.journal_encounters = {}
        self.api_is_configured = False


    def configure_api(self):
        if not  self.api_is_configured:
            self.api = wowapi.WoWApi()
            self.api.lang = self.lang
            self.api.configure()


    def save_all_files(self, dirpath:Path):
        
        for jexpansion_id, jexpansion in self.journal_expansions.items():
            jexpansion.save(dirpath)

        for jinstances_id, jinstances in self.journal_instances.items():
            jinstances.save(dirpath)

        for jencounters_id, jencounters in self.journal_encounters.items():
            jencounters.save(dirpath)


    def journals_to_dic(self, journals):
        dic={}
        for key, val in journals.items():
            dic[key]=val.to_dic()
        return dic

    def journal_expansions_from_dic(self, dic):
        self.journal_expansions = {}
        for key, val in dic.items():
            jexpansion = structures.JournalExpansion()
            jexpansion.from_dic(val)
            self.journal_expansions[key]=jexpansion
    
    def journal_instances_from_dic(self, dic):
        self.journal_instances = {}
        for key, val in dic.items():
            jinstance = structures.JournalInstance()
            jinstance.from_dic(val)
            self.journal_instances[key]=jinstance

    def journal_encounters_from_dic(self, dic):
        self.journal_encounters = {}
        for key, val in dic.items():
            jencounter = structures.JournalEncounter()
            jencounter.from_dic(val)
            self.journal_encounters[key]=jencounter

    def save(self, dirpath:Path):
        data = {}
        data["journal_expansions"]=self.journals_to_dic(self.journal_expansions)
        data["journal_instances"]=self.journals_to_dic(self.journal_instances)
        data["journal_encounters"]=self.journals_to_dic(self.journal_encounters)
        path = dirpath / f"{self.lang}_gamedata.json"
        save(data, path)

    def load(self, dirpath:Path):
        path = dirpath / f"{self.lang}_gamedata.json"
        data = load(path)
        self.journal_expansions_from_dic(data["journal_expansions"])
        self.journal_instances_from_dic(data["journal_instances"])
        self.journal_encounters_from_dic(data["journal_encounters"])


    def get_db_file_path(self, dirpath:Path) -> Path:
        path = dirpath / f"{self.lang}_gamedata.json"
        return path


    # Expansion
    def create_journal_expansion(self, journal_expansion_id) -> structures.JournalExpansion:
        journal = self.api.get_journal_expansion(journal_expansion_id)
        jexpansion = structures.JournalExpansion()
        jexpansion.lang = self.lang
        jexpansion.id = journal_expansion_id
        jexpansion.data = journal
        return jexpansion

    def explore_expansion(self, journal_expansion_id):
        print(f"Explore expansion {journal_expansion_id}")
        jexpansion = self.create_journal_expansion(journal_expansion_id)
        self.journal_expansions[str(jexpansion.id)]=jexpansion

        jinstance_ids = jexpansion.get_instance_ids()
        for jinstance_id in jinstance_ids:
            self.explore_instance(jinstance_id)

    def explore_expansions(self, journal_expansion_ids):
        for journal_expansion_id in journal_expansion_ids:
            self.explore_expansion(journal_expansion_id)

    # Instance
    def create_journal_instance(self, jinstance_id) -> structures.JournalInstance:
        journal = self.api.get_journal_instance(jinstance_id)
        jinstance = structures.JournalInstance()
        jinstance.lang = self.lang
        jinstance.id = jinstance_id
        jinstance.data = journal
        return jinstance

    def explore_instance(self, jinstance_id):
        print(f"-- Explore instance {jinstance_id}")
        jinstance = self.create_journal_instance(jinstance_id)
        self.journal_instances[str(jinstance.id)]=jinstance

        jencounter_ids = jinstance.get_encounter_ids()
        for jencounter_id in jencounter_ids:
            self.explore_encounter(jencounter_id)

    
    # Encounter
    def create_journal_encounter(self, jencounter_id) -> structures.JournalEncounter:
        journal = self.api.get_journal_encounter(jencounter_id)
        jencounter = structures.JournalEncounter()
        jencounter.lang = self.lang
        jencounter.id = jencounter_id
        jencounter.data = journal
        return jencounter

    def explore_encounter(self, jencounter_id):
        print(f"---- Explore encounter {jencounter_id}")
        jencounter = self.create_journal_encounter(jencounter_id)
        self.journal_encounters[str(jencounter.id)]=jencounter    


def explore(journal_expansion_ids, lang:str, dbdir:Path):

    wgd = WowGameData()
    wgd.lang = lang

    # Load if file db exist
    file_db_path = wgd.get_db_file_path(dbdir)
    if file_db_path.exists():
        print(f"File {file_db_path} loading...")
        wgd.load(dbdir)
        print(f"File loaded.")

    # Explore
    print(f"Game data exploring...")
    wgd.configure_api()
    wgd.explore_expansions(journal_expansion_ids)
    print(f"Game data explored.")
    
    # Save result
    print(f"File {file_db_path} saving...")
    wgd.save(dbdir)
    print(f"File saved.")


def print_random_encounter(lang:str, dbdir:Path):
    
    wgd = WowGameData()
    wgd.lang = lang

    # Load if file db exist
    file_db_path = wgd.get_db_file_path(dbdir)
    if file_db_path.exists():
        print(f"File {file_db_path} loading...")
        wgd.load(dbdir)
        print(f"File loaded.")

    # Select an encounter
    rand_key = random.choice(list(wgd.journal_encounters.keys()))
    print(wgd.journal_encounters[rand_key].to_string())
    