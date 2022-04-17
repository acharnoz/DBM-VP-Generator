import json
from abc import ABC, abstractmethod

class AIAudioConfig(ABC):

    def __init__(self):
        self.name = ""
        self.description = ""
        self.aiengine = ""
        
        self.audiogain = 0
        self.audiospeed = 100
                

    def insert_paramaters(self,dic):
        dic["name"] = self.name
        dic["description"] = self.description
        dic["audiogain"] = self.audiogain
        dic["audiospeed"] = self.audiospeed
        dic["aiengine"] = self.aiengine
    
    
    def extract_paramaters(self,dic):
        self.name = dic["name"]
        self.description = dic["description"]
        self.audiogain = dic["audiogain"]
        self.audiospeed = dic["audiospeed"]
        self.aiengine = dic["aiengine"]
        
        
    def load(self, filepath):
        data = {}
        
        with open(filepath, encoding='utf-8') as json_file:    
            data = json.load(json_file)
        
        self.extract_paramaters(data)
          
          
    def save(self, filepath):
        data={}
        
        self.insert_paramaters(data)

        with open(filepath, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4, separators=(',', ': '))


class AIAudioEngine(ABC):
    
    def __init__(self):
        self.config = None
    
    @abstractmethod
    def load_config(self, config_path):
        pass
    
    @abstractmethod
    def save_config(self, config_path):
        pass
        
    @abstractmethod
    def convert_text_to_ogg(self, text, ogg_filepath):
        pass
