from pathlib import Path
from enum import Enum
from datetime import date
import io
from unidecode import unidecode

import shutil

from gamedata import wowgamedata
from gamedata import structures
from vpgenerator import dictionary
from vpgenerator import audiofilestools

class AddonKey(Enum):
    KEY_ADDON_TITLE = 1
    KEY_ADDON_NAME = 2
    KEY_ADDON_VERSION = 3
    KEY_VOICEPACK_NAME = 4
    KEY_INSTANCE_KEY = 5
    KEY_LANG = 6
    KEY_VOICEPACK_VAR = 7
    KEY_SPELLS_LINES = 8
    KEY_INSTANCE_NAME = 9
    KEY_EXPANSION_KEY = 10


class AddonManager:

    def __init__(self):
        today = date.today()
        self.version = today.strftime("%Y%m%d")

        self.expansion_key = ""
        self.instance_key = ""
        self.instance_name = ""
        self.addon_name = ""
        self.addon_lang = ""
        self.wgsd = wowgamedata.WowGameData()

        self.lua_tpl_path = Path("./scripts/gamedata/template/addon.lua")
        self.toc_tpl_path = Path("./scripts/gamedata/template/addon.toc")
        self.addondbpath = Path()
        self.key_to_var = {}

        self.spellkey_to_es = {}

    def set_param(self, instance_key: str, wgsd: wowgamedata.WowGameData, addondbpath: Path):

        self.instance_key = instance_key
        self.wgsd = wgsd
        self.addondbpath = addondbpath

        self.addon_lang = self.wgsd.lang.upper()
        self.instance_name = self.wgsd.journal_instances[instance_key].get_name(
        )
        self.addon_name = "DBMEA" + "-" + \
            self.convert_string(self.instance_name) + "-" + self.addon_lang
        self.expansion_key = self.wgsd.journal_instances[instance_key].get_expansion_id()

        self.key_to_var[AddonKey.KEY_ADDON_TITLE] = unidecode(self.instance_name)
        self.key_to_var[AddonKey.KEY_INSTANCE_NAME] = unidecode(self.instance_name)
        
        self.key_to_var[AddonKey.KEY_ADDON_NAME] = self.addon_name
        self.key_to_var[AddonKey.KEY_VOICEPACK_NAME] = self.addon_name

        self.key_to_var[AddonKey.KEY_ADDON_VERSION] = self.version
        self.key_to_var[AddonKey.KEY_INSTANCE_KEY] = self.instance_key
        self.key_to_var[AddonKey.KEY_EXPANSION_KEY] = str(self.expansion_key)
        self.key_to_var[AddonKey.KEY_LANG] = self.addon_lang

    def convert_string(self, oldstr: str) -> str:
        new_str = unidecode(oldstr)
        new_str = new_str.replace("'", " ")
        new_str = new_str.replace(":", " ")
        new_str = ''.join(x for x in new_str.title() if not x.isspace())
        return new_str

    def create_encounter_spell_lines(self, jencounter_id: str, es: structures.EncounterSpell) -> str:
        sout = io.StringIO()
        section = " ".join(str(x) for x in es.journal_section_ids)
        sout.write(
            f"\n    -- Add spell \"{es.name}\" ({es.id}) journal sections:{section}\n")
        path = f"Interface\\\\AddOns\\\\{self.addon_name}\\\\sounds\\\\{self.instance_key}\\\\{jencounter_id}\\\\{es.id}.ogg"
        sout.write(f"    vp:addSpellPath({jencounter_id},{es.id},\"{path}\")\n")
        return sout.getvalue()

    def create_encounter_lines(self, jencounter_id) -> str:
        jencounter = self.wgsd.journal_encounters[jencounter_id]
        sout = io.StringIO()
        sout.write(
            f"\n\n    -- Encounter \"{jencounter.get_name()}\" ({jencounter.id})\n")
        ess = jencounter.get_encounter_spells()
        for es in ess:
            if es.id not in self.spellkey_to_es:
                self.spellkey_to_es[es.id] = es
                sout.write(self.create_encounter_spell_lines(
                    jencounter_id, es))
        return sout.getvalue()

    def create_encounters_lines(self) -> str:
        jinstance = self.wgsd.journal_instances[self.instance_key]
        sout = io.StringIO()

        sout.write(
            f"\n\n    -- Expansion \"{jinstance.get_expansion_name()}\" ({jinstance.get_expansion_id()})\n\n")
        sout.write(
            f"    -- Instance \"{jinstance.get_name()}\" ({jinstance.id}) ({jinstance.get_instance_type()})\n")
        encounter_ids = jinstance.get_encounter_ids()
        for encounter_id in encounter_ids:
            sout.write(self.create_encounter_lines(str(encounter_id)))
        return sout.getvalue()

    def create_dictionary(self, path: Path):
        print(path)
        dico = dictionary.Dictionary()
        dico.name = self.addon_name
        dico.lang = self.addon_lang
        dico.authors = ["Milho (Dalaran)", "Maseo (Cho\'gall)"]
        dico.version = self.version

        for spellkey, es in self.spellkey_to_es.items():
            sound_path = f"sounds/{self.instance_key}/{es.encounter_id}/{es.id}.ogg"
            if dico.lang == "FR":
                text = f"{es.name}, imminent !"
            elif dico.lang == "EN":
                text = f"{es.name}, soon !"
            else:
                text = f"{es.name}"
            dico.add_or_update_translation(sound_path, text)

        dico.print()
        dico.save(path)

    def create_addon(self, generate_sounds: bool=True):
        print("create_directories")

        self.spellkey_to_es = {}

        addonpath = self.addondbpath / self.addon_name
        Path.mkdir(addonpath, parents=True, exist_ok=True)

        soundpath = addonpath / "sounds"
        Path.mkdir(soundpath, parents=True, exist_ok=True)

        luapath = addonpath / f"{self.addon_name}.lua"
        shutil.copy(self.lua_tpl_path, luapath)

        tocpath = addonpath / f"{self.addon_name}.toc"
        shutil.copy(self.toc_tpl_path, tocpath)

        dictionarypath = addonpath / "dictionary"
        Path.mkdir(dictionarypath, parents=True, exist_ok=True)

        self.key_to_var[AddonKey.KEY_VOICEPACK_VAR] = "vp"
        self.key_to_var[AddonKey.KEY_SPELLS_LINES] = self.create_encounters_lines()

        self.replace_keys(luapath)
        self.replace_keys(tocpath)

        dicopath = dictionarypath / f"dictionary-{self.version}.json"
        self.create_dictionary(dicopath)

        if generate_sounds :
            smalllang = self.addon_lang.lower()
            config = Path(f"G:\\Dev\\WOW-VoicePack-Generator\\my-audio-configs\\aws-{smalllang}-female-cfg.json")
            audiofilestools.create_voicepack(dicopath, "AWS", config, addonpath)


    def replace_keys(self, filepath: Path):

        # Opening our text file in read only
        # mode using the open() function
        with open(filepath, 'r') as file:

            # Reading the content of the file
            # using the read() function and storing
            # them in a new variable
            data = file.read()

            # Searching and replacing the text
            # using the replace() function
            for key, val in self.key_to_var.items():
                data = data.replace(key.name, val)

        # Opening our text file in write only
        # mode to write the replaced content
        with open(filepath, 'w') as file:

            # Writing the replaced data in our
            # text file
            file.write(data)

        # Printing Text replaced
        print("Text replaced")