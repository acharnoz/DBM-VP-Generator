import requests
from pathlib import Path
import argparse

import logging
import os
from pprint import pprint
import json
from vpgenerator import dictionary


#api = WowApi("cf439756d012472980bfd93654e74db5", "s3tw976mXyH58Um4KflY38oS9itRSdp7")

def save(data):
    with open("test.json", 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False,
                  indent=4, separators=(',', ': '))


region = "us"
namespace = f"static-{region}"
api = f"https://{region}.api.blizzard.com"
locale = 'fr_FR'
# locale='en_US'


def create_access_token(client_id, client_secret, region):
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://%s.battle.net/oauth/token' %
                             region, data=data, auth=(client_id, client_secret))
    return response.json()


response = create_access_token(
    "cf439756d012472980bfd93654e74db5", "s3tw976mXyH58Um4KflY38oS9itRSdp7", region)
print(response)

access_token = response["access_token"]

headers = {
    'Authorization': f"Bearer {access_token}",
}

params = {
    'namespace': namespace,
    'locale': locale
}


# endpoint = '/data/wow/journal-expansion/499' # list shadowland raids donjons
# endpoint = '/data/wow/journal-instance/1195' # info sur le sépulcre
# endpoint = '/data/wow/journal-encounter/index' # liste de toutes les rencontres
# endpoint = '/data/wow/journal-encounter/2465' # drop and spell boss
# endpoint = '/data/wow/playable-class/2' # paladin
# endpoint = '/data/wow/playable-specialization/65' # paladin sacré talents
#endpoint = '/data/wow/spell/1022'
def get_info(endpoint):
    print(f"{api}{endpoint}")
    response = requests.get(f"{api}{endpoint}", params=params, headers=headers)
    return response


def get_response(api, id):
    endpoint = f"/data/wow/{api}/{id}"
    response = get_info(endpoint)
    return response


class EncounterSpell:

    def __init__(self, name, spell_id):
        self.spell_name = name
        self.spell_id = spell_id
        self.journal_expansion_id = -1
        self.journal_instance_id = -1
        self.instance_id = -1
        self.journal_encounter_id = -1
        self.journal_section_ids = []

    def to_string(self):
        return f'name:{self.spell_name} id:{self.spell_id} expansion:{self.journal_expansion_id} jinstance:{self.journal_instance_id} instance:{self.instance_id} encounter:{self.journal_encouter_id} sections:{self.journal_section_ids}'


#------------------------------------------------------------------------------
def checkSection(section):

    new_spells = []

    section_id = section["id"]

    if "spell" in section:
        spell_name = section["spell"]["name"]
        spell_id = section["spell"]["id"]
        es = EncounterSpell(spell_name, spell_id)
        new_spells.append(es)

    if "sections" in section:
        for s in section["sections"]:
            new_spells.extend(checkSection(s))

    for es in new_spells:
        es.journal_section_ids.insert(0, section_id)

    return new_spells


#------------------------------------------------------------------------------
def checkJournalEncounter(journal_encounter_id):

    new_spells = []

    encounter = get_response('journal-encounter', journal_encounter_id).json()

    for section in encounter["sections"]:
        new_spells.extend(checkSection(section))

    for s in new_spells:
        s.journal_encounter_id = journal_encounter_id
    
    return new_spells

#------------------------------------------------------------------------------
def checkJournalInstance(journal_instance_id):
    
    new_spells = []

    journalInstance = get_response('journal-instance', journal_instance_id).json()
    instance_id = journalInstance["map"]["id"]

    for encounter in journalInstance["encounters"]:
        journal_encounter_id = encounter["id"]
        new_spells.extend(checkJournalEncounter(journal_encounter_id))

    for s in new_spells:
        s.journal_instance_id = journal_instance_id
        s.instance_id = instance_id
    
    return new_spells


#------------------------------------------------------------------------------
def checkJournalExpansion(journal_expansion_id):

    new_spells = []

    journalExpansion = get_response('journal-expansion', journal_expansion_id).json()

    for instance in journalExpansion["dungeons"]:
        journal_instance_id = instance["id"]
        new_spells.extend(checkJournalInstance(journal_instance_id))
    
    for s in new_spells:
        s.journal_expansion_id = journal_expansion_id

    return new_spells


#------------------------------------------------------------------------------
def create_spell_dic(spells):
    spell_dic = {}
    for es in spells:

        if es.instance_id not in spell_dic:
            spell_dic[es.instance_id] = {}

        if es.spell_id not in spell_dic[es.instance_id]:
            spell_dic[es.instance_id][es.spell_id] = es

    return spell_dic

#------------------------------------------------------------------------------
def create_lua_file(addonName, spell_dic, lang):

    path = f"{addonName}.lua"

    with open(path, 'w', encoding='utf-8') as f:

        f.write(f"\nlocal addonName, addon = ...")
        f.write(f"\naddon = LibStub(\"AceAddon-3.0\"):NewAddon(addon, addonName)")
        f.write(f"\n")
        f.write(f"\n-- called by AceAddon when Addon is fully loaded")
        f.write(f"\nfunction addon:OnInitialize()")
        f.write(f"\n  addon:registerSounds()")
        f.write(f"\nend")
        f.write(f"\n")
        f.write(f"\nfunction addon:OnEnable()")
        f.write(f"\n  -- Called when the addon is enabled")
        f.write(f"\nend")
        f.write(f"\n")
        f.write(f"\nfunction addon:OnDisable()")
        f.write(f"\n  -- Called when the addon is disabled")
        f.write(f"\nend")
        f.write(f"\n")
        f.write(f"\nfunction addon:registerSounds()")
        f.write(f"\n\n  local DBMEA = LibStub(\"AceAddon-3.0\"):GetAddon(\"DBMEA\")")

        for instance_id, dic in spell_dic.items():
            vp_val = f"vp{instance_id}"
            packname = f"{addonName} {instance_id}"
            f.write(f"\n\n\n  local {vp_val} = DBMEA:createEAVoicePack(\"{packname}\", {instance_id}, \"{lang}\")")

            for spell_id, es in dic.items():
                f.write(f"\n\n  -- {es.spell_name}")
                path = f"Interface\\\\AddOns\\\\{addonName}\\\\sounds\\\\{instance_id}\\\\{es.journal_encounter_id}\\\\{spell_id}.ogg"
                f.write(f"\n  {vp_val}:addSpellPath({spell_id},\"{path}\")")

        f.write(f"\n\nend")

#------------------------------------------------------------------------------
def create_dictionary(path, spell_dic, lang):
    dico = dictionary.Dictionary()
    dico.name = path
    dico.lang = lang
    dico.authors = ["Milho (Dalaran)"]
    dico.version = "0.1"

    for instance_id, dic in spell_dic.items():
        for spell_id, es in dic.items():
            sound_path= f"sounds/{instance_id}/{es.journal_encounter_id}/{spell_id}.ogg"
            text = f"{es.spell_name}, imminent !"
            dico.add_or_update_translation(sound_path, text)

    dico.save(path)


#------------------------------------------------------------------------------
def create_files(id_expansion, expansion_short_name, lang, dirpath):
    spells = checkJournalExpansion(id_expansion)
    spell_dic = create_spell_dic(spells)
    file_name = f"{dirpath}\DBMEA-Party-{expansion_short_name}-{lang}"
    create_lua_file(file_name, spell_dic, lang)
    file_name_json = f"{file_name}.json"
    create_dictionary(file_name_json, spell_dic, lang)


#en_US
#es_ES
#fr_FR
#de_DE
#it_IT



#create_files(68,"Classic","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Classic (pas d'ID Spell dispo !)
#create_files(70,"BC","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Burning Crusade (pas d'ID Spell dispo !)
#create_files(72,"WoLK","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Wrath of the Lich King (pas d'ID Spell dispo !)
#create_files(73,"Cataclysm","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Cataclysm (pas d'ID Spell dispo !)
create_files(74,"MoP","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Mists of Pandaria (pas d'ID Spell dispo ! si temple de jade)
create_files(124,"WoD","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Warlords of Draenor
create_files(395,"Legion","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Legion
create_files(396,"BfA","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Battle for Azeroth
create_files(499,"Shadowlands","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Shadowlands
create_files(503,"Dragonflight","FR","G:\Dev\WOW-VoicePack-Generator\\test\dbmea") # Dragonflight