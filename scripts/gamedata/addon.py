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