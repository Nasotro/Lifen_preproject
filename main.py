import os
from models.Document import Document

input_path = os.path.join('data', 'input', 'example.json')
output_path = os.path.join('output', 'output.json')

doc = Document(input_path)
doc.write_all_names_json(output_path)
