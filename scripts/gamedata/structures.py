from pathlib import Path
import json
import io
from collections.abc import Mapping, Sequence


def save(data, path:Path) -> None:
    with open(path, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False,
                  indent=4, separators=(',', ': '))

class EncounterSpell:
    
    def __init__(self, spell_name, spell_id):
        self.name = spell_name
        self.id = spell_id
        self.journal_section_ids = []

    def to_string(self) -> str:
        sout = io.StringIO()
        sout.write(f"Encounter spell\n")
        sout.write(f"id: {self.id}\n")
        sout.write(f"name: {self.name}\n")
        sout.write(f"journal_section_ids: {self.journal_section_ids}\n")
        return sout.getvalue()



class JournalEncounter:

    def __init__(self):
        self.data = {}
        self.id = -1
        self.lang = ""

    def to_dic(self):
        dic = {}
        dic["data"]=self.data
        dic["id"]=self.id
        dic["lang"]=self.lang
        return dic

    def check_data_section(self, section, encounter_spells, section_ids):

        new_sections_ids = [section["id"]]
        new_sections_ids.extend(section_ids)
        
        if "spell" in section:
            spell_name = section["spell"]["name"]
            spell_id = section["spell"]["id"]
            encounter_spell = EncounterSpell(spell_name, spell_id)
            encounter_spell.journal_section_ids = new_sections_ids.copy()
            encounter_spell.journal_section_ids.reverse()
            encounter_spells.append(encounter_spell)

        if "sections" in section:
            for s in section["sections"]:
                self.check_data_section(s, encounter_spells, new_sections_ids)


    def get_encounter_spells(self) -> Sequence[EncounterSpell]:
        encounter_spells = []
        section_ids = []
        if "sections" in self.data:
            for section in self.data["sections"]:
                self.check_data_section(section, encounter_spells, section_ids)
        else:
            print("ERROR")
        return encounter_spells

    
    def from_dic(self, dic):
        self.data=dic["data"]
        self.id=dic["id"]
        self.lang=dic["lang"]

    def save(self, dirpath:Path) -> None:
        path= dirpath / f"{self.lang}" / "JournalEncounter" / f"{self.id}.json"
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        save(self.data, path)
    
    def to_string(self) -> str:
        sout = io.StringIO()
        sout.write(f"Encounter\n")
        sout.write(f"id: {self.id}\n")
        spells = self.get_encounter_spells()
        for s in spells:
            sout.write(s.to_string())
        return sout.getvalue()


class JournalInstance:

    def __init__(self):
        self.data = {}
        self.id = -1
        self.lang = ""
    
    def to_dic(self):
        dic = {}
        dic["data"]=self.data
        dic["id"]=self.id
        dic["lang"]=self.lang
        return dic
    
    def from_dic(self, dic):
        self.data=dic["data"]
        self.id=dic["id"]
        self.lang=dic["lang"]

    def get_encounter_ids(self):
        ids = []
        for encounter in self.data["encounters"]:
            ids.append(encounter["id"])
        return ids
    
    def save(self, dirpath:Path) -> None:
        path= dirpath / f"{self.lang}" / "JournalInstance" / f"{self.id}.json"
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        save(self.data, path)


class JournalExpansion:

    def __init__(self):
        self.data = {}
        self.id = -1
        self.lang = ""
    
    def to_dic(self):
        dic = {}
        dic["data"]=self.data
        dic["id"]=self.id
        dic["lang"]=self.lang
        return dic
    
    def from_dic(self, dic):
        self.data=dic["data"]
        self.id=dic["id"]
        self.lang=dic["lang"]

    def get_dungeons_ids(self):
        ids = []
        for instance in self.data["dungeons"]:
            ids.append(instance["id"])
        return ids

    def get_raids_ids(self):
        ids = []
        for instance in self.data["raids"]:
            ids.append(instance["id"])
        return ids

    def get_instance_ids(self):
        ids = self.get_dungeons_ids()
        ids.extend(self.get_raids_ids())
        return ids

    def save(self, dirpath:Path) -> None:
        path= dirpath / f"{self.lang}" / "JournalExpansion" / f"{self.id}.json"        
        Path.mkdir(path.parent, parents=True, exist_ok=True)
        save(self.data, path)