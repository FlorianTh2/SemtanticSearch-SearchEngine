import random
import pickle

import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from pymongo import MongoClient
import json
from bson import json_util

from ClassifierBasedGermanTagger.ClassifierBasedGermanTagger import ClassifierBasedGermanTagger

class Preprocessor:
    def __init__(self):
        self.stemmer_german = SnowballStemmer('german')
        with open('nltk_german_classifier_data.pickle', 'rb') as f:
        #Lade den neuen alten Tagger in eine neue Instanz
            self.tagger = pickle.load(f)
        self.stop_words = stopwords.words('german')

    def tokenizing_with_sw_and_punc(self,text):
        text = text.lower()
        # tokenize text 
        return word_tokenize(text)
        
    def tokenizing_without_punc(self,text):
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(text)

    def tokenizing_complete(self,text):
        tokenizer = RegexpTokenizer(r'\w+')
        word_tokens = tokenizer.tokenize(text)
        filtered_sentence = [w for w in word_tokens if not w in self.stop_words]
        filtered_sentence = []
        for w in word_tokens:
            if w not in self.stop_words:
                filtered_sentence.append(w)
        filtered_word_tokens = filtered_sentence
        return filtered_word_tokens


    def tokenizing_reverse(self,words):
        return nltk.Text(words)

    def stemming(self,word):
        return self.stemmer_german.stem(word)

    def stemming_words(self,word_tokens):
        stemmed_tokens = []
        for w in word_tokens:
            stemmed_tokens.append(self.stemmer_german.stem(w))
        return stemmed_tokens

    def lemmating(self,words):
        return self.tagger.tag(words)



    

