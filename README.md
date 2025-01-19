# Machine Learning Engineer Challenge Lifen

## Goals
We are trying to predict the patient's first and last names for a given medical report.

### Dataset

Let's imagine we have a dataset with 100k unlabeled documents medical documents. 
For each document we have a json representation that gives us absolute coordinates for each word, for exemple:

```json
{"pages":[{"words":[{"text":"hanche","bbox":{"x_min":0.75,"x_max":0.81,"y_min":0.09,"y_max":0.1}},{"text":"JACQUES","bbox":{"x_min":0.74,"x_max":0.83,"y_min":0.16,"y_max":0.17}},{"text":"pour","bbox":{"x_min":0.57,"x_max":0.61,"y_min":0.09,"y_max":0.1}},{"text":"la","bbox":{"x_min":0.73,"x_max":0.75,"y_min":0.09,"y_max":0.1}},{"text":"en","bbox":{"x_min":0.23,"x_max":0.26,"y_min":0.09,"y_max":0.1}},{"text":"bien","bbox":{"x_min":0.15,"x_max":0.19,"y_min":0.09,"y_max":0.1}},{"text":"consultation","bbox":{"x_min":0.26,"x_max":0.36,"y_min":0.09,"y_max":0.1}},{"text":"Monsieur","bbox":{"x_min":0.36,"x_max":0.44,"y_min":0.09,"y_max":0.1}},{"text":"Jean","bbox":{"x_min":0.44,"x_max":0.48,"y_min":0.09,"y_max":0.1}},{"text":"?","bbox":{"x_min":0.72,"x_max":0.73,"y_min":0.09,"y_max":0.1}},{"text":"droite.","bbox":{"x_min":0.82,"x_max":0.87,"y_min":0.09,"y_max":0.1}},{"text":"revu","bbox":{"x_min":0.19,"x_max":0.23,"y_min":0.09,"y_max":0.1}},{"text":"DUPONT","bbox":{"x_min":0.49,"x_max":0.57,"y_min":0.09,"y_max":0.1}},{"text":"douleur","bbox":{"x_min":0.65,"x_max":0.71,"y_min":0.09,"y_max":0.1}},{"text":"J?ai","bbox":{"x_min":0.12,"x_max":0.15,"y_min":0.09,"y_max":0.1}},{"text":"une","bbox":{"x_min":0.61,"x_max":0.65,"y_min":0.09,"y_max":0.1}},{"text":"Nicolas","bbox":{"x_min":0.67,"x_max":0.73,"y_min":0.16,"y_max":0.17}},{"text":"Docteur","bbox":{"x_min":0.6,"x_max":0.67,"y_min":0.16,"y_max":0.17}}]}],"original_page_count":1,"needs_ocr_case":"no_ocr"}
```

We have the target outputs: first and last names and we want to be able to predict them automatically for each new document.


## Features
- Extracts patient names from medical reports.
- Supports JSON input format.
- Utilizes dictionaries for French words, doctor titles, and first names to improve accuracy.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/Nasotro/Lifen_preproject.git
    cd Lifen_preproject
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
To use the project, follow these steps:

1. Prepare your medical report in JSON format.
2. Place the JSON file in the `data/input/` directory.
3. Run the script to extract patient names:
    ```sh
    python main.py data/input/example.json output/output.json
    ```



## Solution 

### Simple Heuristic

The implementation uses a straightforward heuristic approach to predict names:

1. **First Name Matching**: A comprehensive list of first names from around the world is used to match potential first names in the document. If a word in the document matches a name in the list, it is considered a first name.

2. **Last Name Identification**: Words surrounding the identified first name are analyzed. If these words are not found in a standard dictionary, they are considered potential last names. This helps in filtering out common words that are not names.

3. **Title Filtering**: To address the challenge of multiple names in the document (e.g., the name of a doctor), the heuristic checks the words around the identified names. If these words match a list of titles (e.g., Doctor, Professor), the name is not considered the patient's name.

This approach ensures that the predicted names are more likely to be accurate by filtering out common words and titles.

### Improvements
- Add unit tests.
- User Interface for easy interaction ?
- Security measures to protect patient data.
- Performance optimization.
- Support for additional languages.