import json
import libtools

class Translations:
    
    def __init__(self):
        self.data = {}
        self.defaultvalue = "TODO"
        
    def load(self, filepath):
        with open(filepath, encoding='utf-8') as json_file:    
            self.data = json.load(json_file)
    
    def save(self, filepath):
        with open(filepath, 'w', encoding='utf8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4, separators=(',', ': '))
            
    def get_file_to_text(self, lang):
        file_to_text = {}
        for file, trad in self.data.items():
            file_to_text[file]=trad[lang]
        return file_to_text
    
    def get_files(self):
        return self.data.keys()
    
    def add_file_to_text(self, lang, file_to_text):
        for f, txt in file_to_text.items():
            if f in self.data:
                self.data[f][lang]=txt
            else:
                trad = {}
                trad[lang]=txt
                self.data[f]=trad
                
    def print(self):
        for file, trad in self.data.items():
            print(f"{file}")
            for locale, txt in trad.items():
                print(f"\t{locale}: {txt}")

    def add_file_extension(self,extension):
        new_data={}
        for file, trad in self.data.items():
            new_data[file+extension]=trad
        self.data = new_data
                
    def merge_translations(self, trans):
        for file, trad in trans.data.items():
            if not file in self.data:
                self.data[file]=trad
            else:
                print("Key exist !")
                selftrad=self.data[file]
                for locale, txt in trad.items():
                    if not locale in selftrad:
                        selftrad[locale]=txt
                self.data[file]=selftrad
                
    def delete_non_existent_files(self, dirpath):
        keys_to_remove = []
        
        for file in self.data.keys():
            if not (dirpath/file).exists():
                keys_to_remove.append(file)
        
        for file in keys_to_remove:
            self.data.pop(file)
            print(f"Key '{file}' removed from list.")
            
        print(f"Nb file removed = {len(keys_to_remove)}")
        
    def test_non_existent_files(self, dirpath):
        for file in self.data.keys():
            if not (dirpath/file).exists():
                print(f"File '{file}' does not exists.")
                
    def test_non_existent_keys(self, dirpath, filepaths):
        for filepath in filepaths:
            file = filepath.relative_to(dirpath)
            if not str(file.as_posix()) in self.data.keys():
                print(f"Key '{file}' does not exists.")
    
    def add_data_from_filepaths(self, dirpath, filepaths, lang, use_filename, force):
        for filepath in filepaths:
            file = filepath.relative_to(dirpath)
            key = str(file.as_posix())
            if not key in self.data.keys():
                trad = {}
                if use_filename:
                    trad[lang] = filepath.stem
                else:
                    trad[lang] = self.defaultvalue
                self.data[key] = trad
            else:
                trad = self.data[key]
                if not lang in trad.keys() or force:
                    if use_filename:
                        trad[lang] = filepath.stem
                    else:
                        trad[lang] = self.defaultvalue
                        
    def get_missing_keys(self, trans):
        keys=[]        
        for key in trans.data:
            if key not in self.data:
                keys.append(key)
        return keys
        
    def get_missing_key_langs(self, trans):
        key2langs={}        
        for key in trans.data:
            if key in self.data:
                trad=trans.data[key]
                for lang in trad:
                    if lang not in self.data[key]:
                        if key in key2langs:
                            key2langs[key].append(lang)
                        else:
                            key2langs[key]=[lang]
                    
        return key2langs
        
        
    def get_text_differences(self, trans):
        diff=[]        
        for key in trans.data:
            if key in self.data:
                trad=trans.data[key]
                for lang in trad:
                    if lang in self.data[key]:
                        if not (self.data[key][lang] == trans.data[key][lang]):
                            diff.append([key, lang, self.data[key][lang],trans.data[key][lang]])
                    
        return diff
    
    def check_structure(self):
        if len(self.data) > 0:
            ref_langs=sorted(list(list(self.data.values())[0].keys()))
            
            all_keys_have_langs=True
            for key, values in self.data.items():
                langs=sorted(list(values.keys()))
                if ref_langs != langs:
                    all_keys_have_langs=False
            
            if not all_keys_have_langs:
                raise AssertionError("Bad structure: All keys dont support the same lang")
    
    def get_langs(self):
        self.check_structure()
        if len(self.data) > 0:
            return sorted(list(list(self.data.values())[0].keys()))
        else:
            return []
    
    def add_lang(self, lang, use_filename):
        if lang in self.get_langs():
            raise AssertionError(f"The lang {lang} already exist in the dictionary.")
        
        for key, trad in self.data.items():
            if use_filename:
                trad[lang] = Path(key).stem
            else:
                trad[lang] = self.defaultvalue
    
    def remove_lang(self, lang):
        if lang not in self.get_langs():
            raise AssertionError(f"The lang {lang} not exists in the dictionary.")
        
        for key, trad in self.data.items():
            trad.pop(lang)
    
    def add_lang_trad(self, key, lang, txt, force):
        if key not in self.data:
            self.data[key]={lang:txt}
        else:
            if lang not in self.data[key] or force:
                self.data[key][lang]=txt
            else:
                if self.data[key][lang] == self.defaultvalue:
                    self.data[key][lang]=txt
                elif self.data[key][lang] != txt:    
                     print(f"Problem with [{key},{lang}] val={self.data[key][lang]} newVal={txt}")
    
    def merge(self, trans, force):
        if self.get_langs() != trans.get_langs():
            raise AssertionError(f"Langs are not the same between dictionaries.")
        
        for key, trad in trans.data.items():
            for lang, txt in trad.items():
                self.add_lang_trad(key,lang,txt,force)
                
    def update_trad_from_dico(self, trans, force):
        if self.get_langs() != trans.get_langs():
            raise AssertionError(f"Langs are not the same between dictionaries.")
        
        for key, trad in self.data.items():
            if key in trans.data:
                for lang in trad.keys():
                    self.add_lang_trad(key,lang,trans.data[key][lang],force)

    def translate(self, langsrc, langto, force):
        if langsrc not in self.get_langs() or langto not in self.get_langs():
            raise AssertionError(f"Langs are not the in the dictionary.")
        
        for key in self.data:
            if force or self.data[key][langto] == self.defaultvalue:
                text = self.data[key][langsrc]
                translated_text = libtools.get_translated_text(text, langsrc, langto)
                self.add_lang_trad(key, langto, translated_text, force)
                
                
            
                