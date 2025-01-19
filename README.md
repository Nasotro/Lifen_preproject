# Machine Learning Engineer Challenge Lifen

## Goals
We are trying to predict the patient's first and last names for a given medical report.

### Dataset

Let's imagine we have a dataset with 100k unlabeled documents medical documents. See below 3 examples:


![docs](https://user-images.githubusercontent.com/51329768/253037781-0d834349-9da9-47e9-8108-4cf62912c229.png)



For each document we have a json representation that gives us absolute coordinates for each word, for exemple:

```json
{"pages":[{"words":[{"text":"hanche","bbox":{"x_min":0.75,"x_max":0.81,"y_min":0.09,"y_max":0.1}},{"text":"JACQUES","bbox":{"x_min":0.74,"x_max":0.83,"y_min":0.16,"y_max":0.17}},{"text":"pour","bbox":{"x_min":0.57,"x_max":0.61,"y_min":0.09,"y_max":0.1}},{"text":"la","bbox":{"x_min":0.73,"x_max":0.75,"y_min":0.09,"y_max":0.1}},{"text":"en","bbox":{"x_min":0.23,"x_max":0.26,"y_min":0.09,"y_max":0.1}},{"text":"bien","bbox":{"x_min":0.15,"x_max":0.19,"y_min":0.09,"y_max":0.1}},{"text":"consultation","bbox":{"x_min":0.26,"x_max":0.36,"y_min":0.09,"y_max":0.1}},{"text":"Monsieur","bbox":{"x_min":0.36,"x_max":0.44,"y_min":0.09,"y_max":0.1}},{"text":"Jean","bbox":{"x_min":0.44,"x_max":0.48,"y_min":0.09,"y_max":0.1}},{"text":"?","bbox":{"x_min":0.72,"x_max":0.73,"y_min":0.09,"y_max":0.1}},{"text":"droite.","bbox":{"x_min":0.82,"x_max":0.87,"y_min":0.09,"y_max":0.1}},{"text":"revu","bbox":{"x_min":0.19,"x_max":0.23,"y_min":0.09,"y_max":0.1}},{"text":"DUPONT","bbox":{"x_min":0.49,"x_max":0.57,"y_min":0.09,"y_max":0.1}},{"text":"douleur","bbox":{"x_min":0.65,"x_max":0.71,"y_min":0.09,"y_max":0.1}},{"text":"J?ai","bbox":{"x_min":0.12,"x_max":0.15,"y_min":0.09,"y_max":0.1}},{"text":"une","bbox":{"x_min":0.61,"x_max":0.65,"y_min":0.09,"y_max":0.1}},{"text":"Nicolas","bbox":{"x_min":0.67,"x_max":0.73,"y_min":0.16,"y_max":0.17}},{"text":"Docteur","bbox":{"x_min":0.6,"x_max":0.67,"y_min":0.16,"y_max":0.17}}]}],"original_page_count":1,"needs_ocr_case":"no_ocr"}
```

We have the target outputs: first and last names and we want to be able to predict them automatically for each new document.

## Implementations

### 1. Simple Heuristic

I used a very simple approach for this implementation. I downloaded a list of first names from all over the world and try to match the first names in the document with the list of first names. If the first name is in the list, I consider it as a first name. I then look at the words that are before and after the first name to see if they are words from the dictionnary. If they are, I do not consider them as last names. Otherwise, if they are not in the dictionnary, I consider them as last names, and I have a match.
The other problem I faced, is that in the document, you can find multiple names, like the name of the doctor. I tried to filter them out by looking at the few words around the name and see if they are in a lis of titles (like Doctor, Professor, etc...). If they are, I do not consider the match to be the patient's name.
If the 