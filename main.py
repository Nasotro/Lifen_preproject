import os
from models.Document import Document
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Process input and output file paths.')
parser.add_argument('input_path', type=str, help='Path to the input JSON file')
parser.add_argument('output_path', type=str, help='Path to the output JSON file')

# Parse arguments
args = parser.parse_args()

# Create a Document object and write all extracted names to a JSON file
doc = Document(args.input_path)
doc.write_all_names_json(args.output_path)
