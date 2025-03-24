# Advanced_programming_final_project


# Movie Search App 🎬

This project is a Python-based movie search tool that uses web scraping and natural language processing (NLP) to fetch and process movie data. It allows users to search for movies through a graphical interface.



## 🔧 Dependencies

To run the `web_scraping.ipynb` and extract movie data from the web, make sure you have the following libraries installed:

```python
import requests
from bs4 import BeautifulSoup
from imdb import IMDb
import time
import csv
```

## 🧠 NLP Dependencies

We use the Natural Language Toolkit (NLTK) for text preprocessing and keyword extraction:

```python
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
```

To avoid SSL certificate errors when downloading NLTK data, we use the ssl module to create an unverified HTTPS context:

```python
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

Download the required NLTK resources:

```python
nltk.download('punkt', quiet=True)  
nltk.download('punkt_tab', quiet=True)  
nltk.download('stopwords', quiet=True)  
nltk.download('averaged_perceptron_tagger', quiet=True)  
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
```

## 🚀 Running the App

To use the movie search tool, run the GUI using:
```python
python GUI.py
```
This will open the graphical interface where you can type in a search query. The app will return relevant movie results based on your query. 



