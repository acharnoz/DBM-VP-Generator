import gtts
from pydub import AudioSegment
from pathlib import Path
import tempfile
import googletrans

def convert_text_to_ogg(text, code_language, export_file):

    # Create a tempory file
    temp = tempfile.NamedTemporaryFile(delete=False)

    # Make request to google to get synthesis
    tts = gtts.gTTS(text, lang=code_language)

    # Save the audio file
    tts.save(temp.name)
    
    # Read and convert the audio file
    sound = AudioSegment.from_mp3(temp.name)
    sound.export(export_file, format="ogg")
    
    # Remove the temp file
    temp.close()

def get_translated_text(txt,lang_src,lang_dest):
    translator = googletrans.Translator()
    result="Failed"
    try:
        result=translator.translate(txt, src=lang_src, dest=lang_dest).text
    except TypeError:
        print("TypeError exception")
    return result
    
def translate(trans, lang_src, lang_dest):
    for file, trad in trans.data.items():
        trad = trans.data[file]
        if lang_src in trad:
            if (not lang_dest in trad) or (trad[lang_dest]=="TODO"):
                print(trad[lang_src])
                trad[lang_dest]=get_translated_text(trad[lang_src],lang_src,lang_dest)
                print(f"New traduction in {lang_dest} => {trad[lang_dest]}")
                
def get_ogg_filepaths(dirpath):
    result=[]
    for p in dirpath.glob('**/*.ogg'):
        result.append(p)
    return result
    
   