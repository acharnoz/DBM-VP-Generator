import json
from pathlib import Path
from datetime import date

DUMMY_VALUE = "DUMMY" # Todo mark, when it is detected, dummy text is used to build the voice
USE_ORIGINAL_VOICE = "USE_ORIGINAL_VOICE" # Use the original EN voice
        
class Dictionary:
    
    def __init__(self):
        self.name = "" # Name of dictionary
        self.lang = "" # dictionary lang fr, en, de, etc  
        self.authors = [] # list of string
        self.version = "" # version of dictionary ex v1.0.0
        self.version_date = date.today().strftime("%Y-%m-%d") # version of dictionary ex v1.0.0
        self.VPVEM_reference = "" # version / changeset of VP VEM
        self.dummy_text = "Text has not been translated yet"
        self.description = "" # Description about the dictionary
        self.filename_to_translation = {} # dict file.ogg to text
    
    
    def load(self, filepath):
        with open(filepath, encoding='utf-8') as json_file:    
            data = json.load(json_file)
        
        self.name = data["name"]
        self.lang = data["lang"]
        self.authors = data["authors"]
        self.version = data["version"]
        self.version_date = data["version_date"]
        self.VPVEM_reference = data["VPVEM_reference"]
        self.dummy_text = data["dummy_text"]
        self.description = data["description"]
        self.filename_to_translation = data["filename_to_translation"]
    
    
    def save(self, filepath):
        data={}
        data["name"] = self.name
        data["lang"] = self.lang
        data["authors"] = self.authors
        data["version"] = self.version
        data["version_date"] = date.today().strftime("%Y-%m-%d")
        data["VPVEM_reference"] = self.VPVEM_reference
        data["dummy_text"] = self.dummy_text
        data["description"] = self.description
        data["filename_to_translation"] = self.filename_to_translation
            
        with open(filepath, 'w', encoding='utf8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4, separators=(',', ': '))

    
    def keys(self):
        return self.filename_to_translation.keys()
    
    
    def items(self):
        return self.filename_to_translation.items()

    
    def add_files(self, filepaths, default_translation=DUMMY_VALUE):
        print(filepaths)
        for f in filepaths:
            self.add_or_update_translation(f, default_translation, False)

    
    def add_or_update_translation(self, filepath, text=DUMMY_VALUE, force=False):
        if isinstance(filepath,Path):
            key = str(filepath.as_posix())
        else:
            key = filepath
            
        if (key not in self.filename_to_translation
            or force
            or self.filename_to_translation[key] == DUMMY_VALUE
            or self.filename_to_translation[key] == USE_ORIGINAL_VOICE) :
            self.filename_to_translation[key] = text
        elif (self.filename_to_translation[key] != text):
            print(f"Key {key} already exist in the dictionary and the text is different '{self.filename_to_translation[key]}' != '{text}'")        
    
    
    def get_translation(self, file):
        if not file in self.filename_to_translation:
            raise AssertionError(f"File {file} is not present in dictionary.")
        return self.filename_to_translation[file];
    
    
    def print(self):
        print(f"name: {self.name}")
        print(f"lang: {self.lang}")
        print(f"authors: {self.authors}")
        print(f"version: {self.version}")
        print(f"VPVEM_reference: {self.VPVEM_reference}")
        print(f"dummy_text: {self.dummy_text}")
        print("filename_to_translation")
        for file, translation in self.filename_to_translation.items():
            print(f"    {file}: '{translation}'")
                
    
    # Return the files only present inside the current dico (self object)
    def get_unique_files(self, other_dico):
        unique_files = []
        for k in self.keys():
            if k not in other_dico.filename_to_translation:
                unique_files.append(k)
        return unique_files  
    
    
    # Return the files present inside the both current dicos
    def get_common_files(self, other_dico):
        common_files = []
        for k in self.keys():
            if k in other_dico.filename_to_translation:
                common_files.append(k)
        return common_files


    # Return the files present inside the both current dicos where translation is different
    def get_files_with_text_differences(self, other_dico):
        files_with_text_differences = []
        for f in self.get_common_files(other_dico):
            text_self = self.get_translation(f)
            text_other_dico = other_dico.get_translation(f)
            if text_self != text_other_dico:
                files_with_text_differences.append(f)
        return files_with_text_differences
        
    
    def merge(self, other_dico, force=False):
        if self.lang != other_dico.lang:
            raise AssertionError(f"The lang is not the same between dictionaries.")
        
        for filepath, text in other_dico.items():
            self.add_or_update_translation(filepath, text, force)