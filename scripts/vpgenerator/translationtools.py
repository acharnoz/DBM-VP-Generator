from pathlib import Path
import googletrans
import copy


from vpgenerator import dictionary


def get_translated_text(txt, lang_src, lang_dest):
    translator = googletrans.Translator()
    result = dictionary.DUMMY_VALUE
    try:
        result = translator.translate(txt, src=lang_src, dest=lang_dest).text
    except TypeError:
        print("TypeError exception")
    return result

    
def get_translation(dico, lang_dest):
    new_dico = copy.deepcopy(dico)
    new_dico.lang = lang_dest
    
    for filepath, text in dico.items():
        translated_text = get_translated_text(text, dico.lang, lang_dest)
        new_dico.add_or_update_translation(filepath, translated_text, True)
               
    return new_dico
    
def translate(dicopath, new_lang, outputpath):
    dico = dictionary.Dictionary()
    dico.load(dicopath)
    
    translated_dico = get_translation(dico, new_lang)
    translated_dico.save(outputpath)
    