import gtts
from pydub import AudioSegment
from pathlib import Path
import tempfile


from vpgenerator import audioeffects
from vpgenerator import aiaudioengine


GTTS_ENGINE = "GTTS"


class GttsAudioConfig(aiaudioengine.AIAudioConfig):


    def __init__(self):
        super().__init__()
        self.aiengine = GTTS_ENGINE
        self.gttslang = "en"
        self.gttsdomain = "com"
    
    
    def insert_paramaters(self,dic):
        super().insert_paramaters(dic)
        dic["gttslang"] = self.gttslang
        dic["gttsdomain"] = self.gttsdomain
    
    
    def extract_paramaters(self,dic):
        super().extract_paramaters(dic)
        self.gttslang = dic["gttslang"]
        self.gttsdomain = dic["gttsdomain"]


class GttsAudioEngine(aiaudioengine.AIAudioEngine):

    
    def __init__(self):
        self.config = GttsAudioConfig()
    
    
    def load_config(self, config_path):
        self.config = GttsAudioConfig()
        self.config.load(config_path)
    
    def save_config(self, config_path):
        self.config.save(config_path)
    
    
    #Local accent | Language code (lang) | Top-level domain (tld)
    #English (Australia)|en|com.au|
    #English (United Kingdom)|en|co.uk|
    #English (United States)|en|com (default)
    #English (Canada)|en|ca
    #English (India)|en|co.in
    #English (Ireland)|en|ie
    #English (South Africa)|en|co.za
    #French (Canada)|fr|ca
    #French (France)|fr|fr
    #Mandarin (China Mainland)|zh-CN|any
    #Mandarin (Taiwan)|zh-TW|any
    #Portuguese (Brazil)|pt|com.br
    #Portuguese (Portugal)|pt|pt
    #Spanish (Mexico)|es|com.mx
    #Spanish (Spain)|es|es
    #Spanish (United States)|es|com (default)
    def convert_text_to_ogg(self, text, ogg_filepath):

        # Create a tempory file
        temp = tempfile.NamedTemporaryFile(delete=False)

        # Make request to google to get synthesis
        tts = gtts.gTTS(text, lang= self.config.gttslang, tld= self.config.gttsdomain)
        
        # Save the audio file
        tts.save(temp.name)
        
        # Read and convert the audio file
        sound = AudioSegment.from_mp3(temp.name)
        sound.export(ogg_filepath, format="ogg")
        
        
        audioeffects.update_ogg_audio_gain(ogg_filepath,  self.config.audiogain)
        audioeffects.update_ogg_audio_speed(ogg_filepath,  self.config.audiospeed/100)
        
        # Remove the temp file
        temp.close()