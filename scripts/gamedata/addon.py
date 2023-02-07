from pathlib import Path
from enum import Enum
from datetime import date
import shutil

# class syntax


class AddonKey(Enum):
    KEY_ADDON_TITLE = 1
    KEY_ADDON_NAME = 2
    KEY_ADDON_VERSION = 3
    KEY_VOICEPACK_NAME = 4
    KEY_INSTANCE_ID = 5
    KEY_LANG = 6
    KEY_VOICEPACK_VAR = 7
    KEY_SPELLS_LINES = 8
    KEY_INSTANCE_NAME = 9


class AddonManager:

    def __init__(self):
        self.name = ""
        self.date = ""
        self.version = ""
        self.instance_id = ""
        self.lua_tpl_path = Path("./scripts/gamedata/template/addon.lua")
        self.toc_tpl_path = Path("./scripts/gamedata/template/addon.toc")
        self.addondbpath = Path()
        self.key_to_var = {}

    def create_directories(self):
        print("create_directories")

        self.name = "MyAddon"

        addonpath = self.addondbpath / self.name
        Path.mkdir(addonpath, parents=True, exist_ok=True)

        soundpath = addonpath / "sounds"
        Path.mkdir(soundpath, parents=True, exist_ok=True)

        luapath = addonpath / f"{self.name}.lua"
        shutil.copy(self.lua_tpl_path, luapath)

        tocpath = addonpath / f"{self.name}.toc"
        shutil.copy(self.toc_tpl_path, tocpath)

        dictionarypath = addonpath / "dictionary"
        Path.mkdir(dictionarypath, parents=True, exist_ok=True)


        self.key_to_var[AddonKey.KEY_ADDON_TITLE] = self.name
        self.key_to_var[AddonKey.KEY_ADDON_NAME] = self.name
        
        today = date.today()
        d1 = today.strftime("%Y%m%d")
        self.key_to_var[AddonKey.KEY_ADDON_VERSION] = d1
        self.key_to_var[AddonKey.KEY_VOICEPACK_NAME] = self.name
        self.key_to_var[AddonKey.KEY_INSTANCE_ID] = "158"
        self.key_to_var[AddonKey.KEY_LANG] = "FR"
        self.key_to_var[AddonKey.KEY_VOICEPACK_VAR] = "KEY_VOICEPACK_VAR"
        self.key_to_var[AddonKey.KEY_SPELLS_LINES] = "--comment"
        self.key_to_var[AddonKey.KEY_INSTANCE_NAME] = "Instance name toto"

        self.replace_keys(luapath)
        self.replace_keys(tocpath)

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


# # ------------------------------------------------------------------------------
# def create_lua_file(addonName, spell_dic, lang):

#     path = f"{addonName}.lua"

#     with open(path, 'w', encoding='utf-8') as f:

#         f.write(f"\nlocal addonName, addon = ...")
#         f.write(f"\naddon = LibStub(\"AceAddon-3.0\"):NewAddon(addon, addonName)")
#         f.write(f"\n")
#         f.write(f"\n-- called by AceAddon when Addon is fully loaded")
#         f.write(f"\nfunction addon:OnInitialize()")
#         f.write(f"\n  addon:registerSounds()")
#         f.write(f"\nend")
#         f.write(f"\n")
#         f.write(f"\nfunction addon:OnEnable()")
#         f.write(f"\n  -- Called when the addon is enabled")
#         f.write(f"\nend")
#         f.write(f"\n")
#         f.write(f"\nfunction addon:OnDisable()")
#         f.write(f"\n  -- Called when the addon is disabled")
#         f.write(f"\nend")
#         f.write(f"\n")
#         f.write(f"\nfunction addon:registerSounds()")
#         f.write(f"\n\n  local DBMEA = LibStub(\"AceAddon-3.0\"):GetAddon(\"DBMEA\")")

#         for instance_id, dic in spell_dic.items():
#             vp_val = f"vp{instance_id}"
#             packname = f"{addonName} {instance_id}"
#             f.write(
#                 f"\n\n\n  local {vp_val} = DBMEA:createEAVoicePack(\"{packname}\", {instance_id}, \"{lang}\")")

#             for spell_id, es in dic.items():
#                 f.write(f"\n\n  -- {es.spell_name}")
#                 path = f"Interface\\\\AddOns\\\\{addonName}\\\\sounds\\\\{instance_id}\\\\{es.journal_encounter_id}\\\\{spell_id}.ogg"
#                 f.write(f"\n  {vp_val}:addSpellPath({spell_id},\"{path}\")")

#         f.write(f"\n\nend")

# # ------------------------------------------------------------------------------


# def create_dictionary(path, spell_dic, lang):
#     dico = dictionary.Dictionary()
#     dico.name = path
#     dico.lang = lang
#     dico.authors = ["Milho (Dalaran)"]
#     dico.version = "0.1"

#     for instance_id, dic in spell_dic.items():
#         for spell_id, es in dic.items():
#             sound_path = f"sounds/{instance_id}/{es.journal_encounter_id}/{spell_id}.ogg"
#             text = f"{es.spell_name}, imminent !"
#             dico.add_or_update_translation(sound_path, text)

#     dico.save(path)


# # ------------------------------------------------------------------------------
# def create_files(id_expansion, expansion_short_name, lang, dirpath):
#     spells = checkJournalExpansion(id_expansion)
#     spell_dic = create_spell_dic(spells)
#     file_name = f"{dirpath}\DBMEA-Party-{expansion_short_name}-{lang}"
#     create_lua_file(file_name, spell_dic, lang)
#     file_name_json = f"{file_name}.json"
#     create_dictionary(file_name_json, spell_dic, lang)
