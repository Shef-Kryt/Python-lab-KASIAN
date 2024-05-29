import re
import numpy as np
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import gensim
import os
import json
from django.http import JsonResponse
corpus = []
MODEL_PATH = "Downloads/myenv/venv/word2vec_model"
def update_corpus(new_text):
    global corpus
    cleaned_text = clean_text(new_text)
    tokens = preprocess_text(cleaned_text)
    corpus.extend(tokens)
    model = Word2Vec(sentences=[corpus], vector_size=100, window=5, min_count=1, workers=4)
    model.train([corpus], total_examples=len(corpus), epochs=10)
    model.save(MODEL_PATH)
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    return text
def preprocess_text(record: str) -> list:
    tokens = word_tokenize(record.lower())
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    return stemmed_tokens
def add_record_to_corpus(new_record):
    words = word_tokenize(record.content)
    for word in words:
        cleaned_word = clean_text(word)
        if cleaned_word:
            keyword, created = Keyword.objects.get_or_create(word=cleaned_word)
            if not created:
                keyword.frequency += 1
                keyword.save()
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
def add_keyword_to_json(file_path, keyword):
    data = read_json_file(file_path)
    data.append(keyword)
    write_json_file(file_path, data)
def update_keyword_in_json(file_path, index, new_keyword):
    data = read_json_file(file_path)
    if 0 <= index < len(data):
        data[index] = new_keyword
        write_json_file(file_path, data)
def delete_keyword_from_json(file_path, index):
    data = read_json_file(file_path)
    if 0 <= index < len(data):
        data.pop(index)
        write_json_file(file_path, data)


