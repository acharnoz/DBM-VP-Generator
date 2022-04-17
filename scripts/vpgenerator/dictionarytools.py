from pathlib import Path
import os

from vpgenerator import dictionary


def create_dico(addondir, lang, name, dicopath):
    dico = dictionary.Dictionary()
    dico.name = name
    dico.lang = lang
    filepaths = [f.relative_to(addondir) for f in addondir.glob('**/*.ogg')]
    dico.add_files(filepaths)   
    #dico.print()
    dico.save(dicopath)


def compare_dicos(dicoA_path, dicoB_path):
    
    dicoA = dictionary.Dictionary()
    dicoA.load(dicoA_path)
    
    dicoB = dictionary.Dictionary()
    dicoB.load(dicoB_path)
    
    if dicoA.lang != dicoB.lang:
        print(f"Dico lang are different: {dicoA.lang} != {dicoB.lang}")
    
    files = dicoA.get_unique_files(dicoB)
    if len(files) > 0 :
        print(f"Unique files in {dicoA.name}")
        for f in files:
            print(f"    {f}")
    
    files = dicoB.get_unique_files(dicoA)
    if len(files) > 0 :
        print(f"Unique files in {dicoB.name}")
        for f in files:
            print(f"    {f}")
            
    files = dicoA.get_files_with_text_differences(dicoB)
    if len(files) > 0 :
        print(f"Text differences for {dicoA.name} and {dicoB.name}")
        for f in files:
            print(f"    {f}: '{dicoA.get_translation(f)}' != '{dicoB.get_translation(f)}'")

          
def merge_dico(dicoA_path, dicoB_path, dico_out_path, force):    
    dicoA = dictionary.Dictionary()
    dicoA.load(dicoA_path)
    
    dicoB = dictionary.Dictionary()
    dicoB.load(dicoB_path)
    
    dicoA.merge(dicoB, force)
    
    dicoA.save(dico_out_path) 
    