import json
import pandas as pd
import os

class Document:
    def __init__(self, path):
        self.path = path
        self.pages = [Page(page) for page in json.load(open(path))['pages']]
    
    def get_all_names(self):
        names = []
        for page in self.pages:
            names.append(page.get_name())
        return names
    
    def write_all_names_json(self, output_path):
        all_names = self.get_all_names()
        names = {"names":all_names}
        with open(output_path, 'w') as f:
            json.dump(names, f)
    
    def __getitem__(self, i):
        return self.pages[i]
    
    def __repr__(self):
        return f'Document({self.path})'
    def __str__(self):
        return f'Document({self.path})'

class Page:
    def __init__(self, data):
        self.data = data
        self.words = [Word(word) for word in self.data['words']]
        self.sorted_doc = self.get_all_text()
        self.sorted_doc_text = [word.word for word in self.sorted_doc]
        self.load_dicts()

    def load_dicts(self):
        dicts = Dicts("data/francais.txt", "data/Doctors.json", "data/Prenoms.csv")
        self.dicts = dicts
        self.dico_fr = dicts.dico_fr
        self.doctor_title = dicts.doctor_title
        self.prenoms = dicts.prenoms
        self.forbidden_words = self.doctor_title

    def get_all_text(self):
        return sorted(self.words, key=lambda x: (x.positions[1], x.positions[0]))

    def get_name(self):
        if not self.dicts:
            raise ValueError('No dictionaries loaded')
        name = {}
        text = self.sorted_doc_text
        for i, word in enumerate(text):
            if word.lower() in self.prenoms:
                if i>0 and i<len(text)-1:
                    if self.check_forbidden_word_in_range(i):
                        if text[i-1].lower() not in self.dico_fr:
                            name["first_name"] = text[i]
                            name["last_name"] = text[i-1]
                        if text[i+1].lower() not in self.dico_fr:
                            name["first_name"] = text[i]
                            name["last_name"] = text[i+1]
                    else: continue # next word
        return name
    
    def check_forbidden_word_in_range(self, i, r=3):
        for j in range(r):
            if(i>j):
                if(self.sorted_doc_text[i-j].lower() in self.forbidden_words):
                    return False
        return True

    def __repr__(self):
        return f'Page({self.words})'
    def __str__(self):
        return f'Page({self.words})'

class Word:
    def __init__(self, json_word):
        self.json_word = json_word
        self.word = json_word['text']
        self.bbox = json_word['bbox']
        self.positions = self.bbox['x_min'], self.bbox['y_min'], self.bbox['x_max'], self.bbox['y_max']
        self.pos = (self.bbox['x_min'] + self.bbox['x_max']) / 2, (self.bbox['y_min'] + self.bbox['y_max']) / 2
        
    def __repr__(self): 
        return f'Word({self.word}, {self.positions})'
    
    def __str__(self):
        return f'Word({self.word}, {self.positions})'
    
class Dicts:
    def __init__(self, dico_fr_path = None, doctors_path = None, prenoms_path = None):
        self.dico_fr = self.load_dico_fr(dico_fr_path) if dico_fr_path else None
        self.doctor_title = self.load_doctors(doctors_path) if doctors_path else None
        self.prenoms = self.load_prenoms(prenoms_path) if prenoms_path else None
        
    def load_dico_fr(self, dico_fr_path):
        dico_fr = []
        with open(dico_fr_path, 'r') as f:
            for line in f:
                dico_fr.append(line.strip())
        return set(dico_fr)
    
    def load_doctors(self, doctors_path):
        return list(json.load(open(doctors_path, encoding='UTF-8'))['metiers_medicaux'])
    
    def load_prenoms(self, prenoms_path):
        prenoms_df = pd.read_csv(prenoms_path, sep=';')
        def remove_parenthesis(name):
            if isinstance(name, str) and '(' in name:
                return name.split('(')[0].strip()
            return name
        return prenoms_df['01_prenom'].apply(remove_parenthesis).unique()

    def __repr__(self):
        return f'Dicts({self.dico_fr}, {self.doctor_title}, {self.prenoms})'
    def __str__(self):
        return f'Dicts({self.dico_fr}, {self.doctor_title}, {self.prenoms})'


input_path = os.path.join('input', 'example.json')
output_path = os.path.join('output', 'output.json')

doc = Document(input_path)
doc.write_all_names_json(output_path)
