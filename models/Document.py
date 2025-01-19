import json
import pandas as pd

class Document:
    """
    A class representing a document containing multiple pages.

    Attributes:
        path (str): The file path to the JSON representation of the document.
        pages (list): A list of Page objects representing each page in the document.
    
    Functions:
        get_all_names: Retrieves all names from each page in the document.
        write_all_names_json: Writes all extracted names to a JSON file.    
    """

    def __init__(self, path):
        """
        Initializes the Document object with the given file path.

        Args:
            path (str): The file path to the JSON representation of the document.
        """
        self.path = path
        self.pages = [Page(page) for page in json.load(open(path))['pages']]

    def get_all_names(self):
        """
        Retrieves all names from each page in the document.

        Returns:
            list: A list of names extracted from each page.
        """
        names = []
        for page in self.pages:
            names.append(page.get_name())
        return names

    def write_all_names_json(self, output_path):
        """
        Writes all extracted names to a JSON file.

        Args:
            output_path (str): The file path where the JSON output will be saved.
        """
        all_names = self.get_all_names()
        names = {"names": all_names}
        with open(output_path, 'w') as f:
            json.dump(names, f)
        print(f'Names extracted from document saved to {output_path}')

    def __getitem__(self, i):
        return self.pages[i]

    def __repr__(self):
        return f'Document({self.path})'

    def __str__(self):
        return f'Document({self.path})'

class Page:
    """
    A class representing a page in a document.

    Attributes:
        data (dict): The JSON data representing the page.
        words (list): A list of Word objects representing each word on the page.
        sorted_doc (list): A list of Word objects sorted by their positions.
        sorted_doc_text (list): A list of strings representing the text of each word in sorted_doc.
        dicts (Dicts): An instance of the Dicts class containing various dictionaries.
        dico_fr (set): A set of French words.
        doctor_title (set): A set of doctor titles.
        prenoms (set): A set of first names.
        forbidden_words (set): A set of forbidden words (doctor titles).
    """

    def __init__(self, data):
        """
        Initializes the Page object with the given data.

        Args:
            data (dict): The JSON data representing the page.
        """
        self.data = data
        self.words = [Word(word) for word in self.data['words']]
        self.sorted_doc = self.get_all_text()
        self.sorted_doc_text = [word.word for word in self.sorted_doc]
        self.load_dicts()

    def load_dicts(self):
        """
        Loads various dictionaries needed for name extraction.
        """
        dicts = Dicts("data/dictionaries/francais.txt", "data/dictionaries/Doctors.json", "data/dictionaries/Prenoms.csv")
        self.dicts = dicts
        self.dico_fr = dicts.dico_fr
        self.doctor_title = dicts.doctor_title
        self.prenoms = dicts.prenoms
        self.forbidden_words = self.doctor_title

    def get_all_text(self):
        """
        Sorts all words on the page by their positions.

        Returns:
            list: A list of Word objects sorted by their positions.
        """
        return sorted(self.words, key=lambda x: (x.positions[1], x.positions[0]))

    def get_name(self):
        """
        Extracts the first and last names from the sorted text on the page.

        Returns:
            dict: A dictionary containing the extracted first and last names.
        """
        if not self.dicts:
            raise ValueError('No dictionaries loaded')
        name = {}
        text = self.sorted_doc_text
        for i, word in enumerate(text):
            if word.lower() in self.prenoms:
                if 0 < i < len(text) - 1:
                    if self.check_forbidden_word_in_range(i):
                        if text[i-1].lower() not in self.dico_fr:
                            name["first_name"] = text[i]
                            name["last_name"] = text[i-1]
                        if text[i+1].lower() not in self.dico_fr:
                            name["first_name"] = text[i]
                            name["last_name"] = text[i+1]
                    else:
                        continue  # next word
        return name

    def check_forbidden_word_in_range(self, i, r=3):
        """
        Checks if there are any forbidden words within a specified range around the given index.

        Args:
            i (int): The index of the word to check around.
            r (int): The range to check for forbidden words.

        Returns:
            bool: True if no forbidden words are found within the range, False otherwise.
        """
        for j in range(r):
            if i > j:
                if self.sorted_doc_text[i-j].lower() in self.forbidden_words:
                    return False
        return True

    def __repr__(self):
        return f'Page({self.words})'
    def __str__(self):
        return f'Page({self.words})'

class Word:
    """
    A class representing a word in a document.

    Attributes:
        json_word (dict): The JSON data representing the word.
        word (str): The text of the word.
        bbox (dict): The bounding box coordinates of the word.
        positions (tuple): A tuple containing the coordinates (x_min, y_min, x_max, y_max) of the word.
        pos (tuple): A tuple containing the center position (x, y) of the word.
    """

    def __init__(self, json_word):
        """
        Initializes the Word object with the given JSON data.

        Args:
            json_word (dict): The JSON data representing the word.
        """
        self.json_word = json_word
        self.word = json_word['text']
        self.bbox = json_word['bbox']
        self.positions = (self.bbox['x_min'], self.bbox['y_min'], self.bbox['x_max'], self.bbox['y_max'])
        self.pos = ((self.bbox['x_min'] + self.bbox['x_max']) / 2, (self.bbox['y_min'] + self.bbox['y_max']) / 2)

    def __repr__(self): 
        return f'Word({self.word}, {self.positions})'
    
    def __str__(self):
        return f'Word({self.word}, {self.positions})'
    
class Dicts:
    """
    A class representing various dictionaries used for name extraction.

    Attributes:
        dico_fr (set): A set of French words.
        doctor_title (list): A list of doctor titles.
        prenoms (set): A set of first names.
    """

    def __init__(self, dico_fr_path=None, doctors_path=None, prenoms_path=None):
        """
        Initializes the Dicts object with the given file paths.

        Args:
            dico_fr_path (str): The file path to the French words dictionary.
            doctors_path (str): The file path to the doctors titles JSON file.
            prenoms_path (str): The file path to the first names CSV file.
        """
        self.dico_fr = self.load_dico_fr(dico_fr_path) if dico_fr_path else None
        self.doctor_title = self.load_doctors(doctors_path) if doctors_path else None
        self.prenoms = self.load_prenoms(prenoms_path) if prenoms_path else None

    def load_dico_fr(self, dico_fr_path):
        """
        Loads the French words dictionary from the given file path.

        Args:
            dico_fr_path (str): The file path to the French words dictionary.

        Returns:
            set: A set of French words.
        """
        dico_fr = []
        with open(dico_fr_path, 'r') as f:
            for line in f:
                dico_fr.append(line.strip())
        return set(dico_fr)

    def load_doctors(self, doctors_path):
        """
        Loads the doctor titles from the given JSON file path.

        Args:
            doctors_path (str): The file path to the doctors titles JSON file.

        Returns:
            list: A list of doctor titles.
        """
        return list(json.load(open(doctors_path, encoding='UTF-8'))['metiers_medicaux'])

    def load_prenoms(self, prenoms_path):
        """
        Loads the first names from the given CSV file path.

        Args:
            prenoms_path (str): The file path to the first names CSV file.

        Returns:
            set: A set of first names.
        """
        prenoms_df = pd.read_csv(prenoms_path, sep=';')

        def remove_parenthesis(name):
            """
            Removes parenthesis and any text within them from a name.

            Args:
                name (str): The name to process.

            Returns:
                str: The processed name.
            """
            if isinstance(name, str) and '(' in name:
                return name.split('(')[0].strip()
            return name

        return prenoms_df['01_prenom'].apply(remove_parenthesis).unique()
    
    def __repr__(self):
        return f'Dicts({self.dico_fr}, {self.doctor_title}, {self.prenoms})'
    def __str__(self):
        return f'Dicts({self.dico_fr}, {self.doctor_title}, {self.prenoms})'

