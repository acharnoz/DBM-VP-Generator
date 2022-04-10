from pathlib import Path
import os

import libtranslations
import libtools

def create_dico(addondirpath, lang, dicopath, usefilename):
    trans = libtranslations.Translations()
    oggfilepaths=libtools.get_ogg_filepaths(addondirpath)
    trans.add_data_from_filepaths(addondirpath, oggfilepaths, lang, usefilename, False)
    #trans.print()
    trans.save(dicopath)

def compare_dicos(dicoA_path, dicoB_path):
    transA = libtranslations.Translations()
    transA.load(dicoA_path)
    transB = libtranslations.Translations()
    transB.load(dicoB_path)
    
    keys = transA.get_missing_keys(transB)
    if len(keys) > 0 :
        print(f"Missing keys in {dicoA_path}")
        for key in keys:
            print(f"    {key}")
    
    keys = transB.get_missing_keys(transA)
    if len(keys) > 0 :
        print(f"Missing keys in {dicoB_path}")
        for key in keys:
            print(f"    {key}")
            
            
    key2langs = transA.get_missing_key_langs(transB)
    if len(key2langs) > 0 :
        print(f"Missing langs in {dicoA_path}")
        for key,langs in key2langs.items():
            print(f"    {key}: {langs}")
     
    key2langs = transB.get_missing_key_langs(transA)
    if len(key2langs) > 0 :
        print(f"Missing langs in {dicoB_path}")
        for key,langs in key2langs.items():
            print(f"    {key}: {langs}")
            
    diff = transA.get_text_differences(transB)
    if len(diff) > 0 :
        print(f"Not corresponding langs between {dicoA_path} and {dicoB_path}")
        for elem in diff:
            print(f"    {elem}")    
 

def add_lang_dico(dico_in_path, dico_out_path, lang, usefilename):
    trans = libtranslations.Translations()
    trans.load(dico_in_path)
    langs = trans.get_langs()
    if lang not in langs:
        trans.add_lang(lang, usefilename)
        trans.save(dico_out_path)
    else:
        print(f"Process aborded, lang '{lang}' already exists.")
        
def remove_lang_dico(dico_in_path, dico_out_path, lang):
    trans = libtranslations.Translations()
    trans.load(dico_in_path)
    langs = trans.get_langs()
    if lang in langs:
        trans.remove_lang(lang)
        trans.save(dico_out_path)
    else:
        print(f"Process aborded, lang '{lang}' does not exist.")

def merge_dico(dico_A_path, dico_B_path, dico_out_path, force):    
    transA = libtranslations.Translations()
    transA.load(dico_A_path)
    transB = libtranslations.Translations()
    transB.load(dico_B_path)
    transA.merge(transB, force)
    transA.save(dico_out_path)    

def update_trad_from_dico(dico_A_path, dico_B_path, dico_out_path, force):    
    transA = libtranslations.Translations()
    transA.load(dico_A_path)
    transB = libtranslations.Translations()
    transB.load(dico_B_path)
    transA.update_trad_from_dico(transB, force)
    transA.save(dico_out_path) 
    
def translate(dico_in_path, langsrc, langto, dico_out_path, force):
    trans = libtranslations.Translations()
    trans.load(dico_in_path)
    langs = trans.get_langs()
    if langsrc in langs and langto in langs:
        trans.translate(langsrc, langto, force)
        trans.save(dico_out_path)
    else:
        print(f"Process aborded, langs '{langsrc}' or '{langto}' does not exist.")

def generate_ogg_files_with_gtts(dico, lang, domain, outputdir):
    trans = libtranslations.Translations()
    trans.load(dico)
    
    for key in trans.data:
        text = trans.data[key][lang]
        export_file = outputdir/Path(key)
        export_file.parent.mkdir(parents=True, exist_ok=True)
        if export_file.exists():
            os.remove(export_file)
        libtools.convert_text_to_ogg_with_gtts(text, lang, domain, export_file)

def generate_ogg_file_with_gtts(dico, lang, domain, key, outputdir):
    trans = libtranslations.Translations()
    trans.load(dico)
    
    text = trans.data[key][lang]
    export_file = outputdir/Path(key)
    export_file.parent.mkdir(parents=True, exist_ok=True)
    if export_file.exists():
        os.remove(export_file)
    libtools.convert_text_to_ogg_with_gtts(text, lang, domain, export_file)