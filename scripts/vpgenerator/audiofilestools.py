from pathlib import Path
import os

from vpgenerator import dictionary
from vpgenerator import gttsengine
from vpgenerator import awsengine


def create_engine(engine_name, configpath):
    # Create engine
    engine = ""
    if engine_name == gttsengine.GTTS_ENGINE:
        engine = gttsengine.GttsAudioEngine()
    elif engine_name == awsengine.AWS_ENGINE:
        engine = awsengine.AwsAudioEngine()
    
    # Manage AI engine
    if configpath is not None:
        engine.load_config(configpath)
        
    return engine


def create_voice(text, engine_name, configpath, oggfilepath):
    if oggfilepath.exists():
            os.remove(oggfilepath)
    engine = create_engine(engine_name, configpath)
    engine.convert_text_to_ogg(text, oggfilepath)


def create_voice_from_voicepack(dummy_text, engine, text, oggfilepath):
    if text == dictionary.DUMMY_VALUE:
        text = dummy_text
        print(f"[WARN] File {oggfilepath} is generated with DUMMY text.")
        
    if text == dictionary.USE_ORIGINAL_VOICE:
        print(f"[WARN] File {oggfilepath} is not generated (USE_ORIGINAL_VOICE).")
    
    else:
        oggfilepath.parent.mkdir(parents=True, exist_ok=True)
        if oggfilepath.exists():
            os.remove(oggfilepath)
        
        engine.convert_text_to_ogg(text, oggfilepath)


def create_voices_from_files( files, dico, engine, outputdirpath):
    num = 0
    nb_files = len(files)
    for file in files:
        num = num + 1
        oggfilepath = outputdirpath/Path(file)
        print(f"File {file} converted ({num}/{nb_files})")
        create_voice_from_voicepack(dico.dummy_text, engine, dico.get_translation(file), oggfilepath)
        
        

def create_voicepack(dicopath, engine_name, configpath, outputdirpath):
    dico = dictionary.Dictionary()
    dico.load(dicopath)
    
    engine = create_engine(engine_name, configpath)
    
    create_voices_from_files(dico.keys(), dico, engine, outputdirpath)
    
    dicoreference = outputdirpath/Path('dictionary.json')
    dico.save(dicoreference)
        
        
def update_voicepack(dicopath, olddicopath, engine_name, configpath, outputdirpath):
    dico = dictionary.Dictionary()
    dico.load(dicopath)
    
    olddico = dictionary.Dictionary()
    olddico.load(olddicopath)
    
    engine = create_engine(engine_name, configpath)
    
    # Generate new keys
    print("Generate new keys:")
    files = dico.get_unique_files(olddico)
    create_voices_from_files(files, dico, engine, outputdirpath)
    
    # Generate updated keys
    print("Generate updated keys:")
    files = dico.get_files_with_text_differences(olddico)    
    create_voices_from_files(files, dico, engine, outputdirpath)
    
    dicoreference = outputdirpath/Path('dictionary.json')
    dico.save(dicoreference)