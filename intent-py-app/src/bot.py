'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import string
import re
import joblib
import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Dense, Flatten, Conv1D, MaxPooling1D
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping


def frame_data(feat_1, feat_2, is_pattern):
    is_pattern = is_pattern
    df = pd.DataFrame(columns=[feat_1, feat_2])
    for intent in data['intents']:
        if is_pattern:
            for pattern in intent['patterns']:
                w = pattern
                df_to_append = pd.Series([w, intent['tag']], index=df.columns)
                df = df.append(df_to_append, ignore_index=True)
        else:
            for response in intent['responses']:
                w = response
                df_to_append = pd.Series([w, intent['tag']], index=df.columns)
                df = df.append(df_to_append, ignore_index=True)
    return df

def tokenizer(entry):
    tokens = entry.split()
    re_punc = re.compile('[%s]' % re.escape(string.punctuation))
    tokens = [re_punc.sub('', w) for w in tokens]
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [lemmatizer.]
    '''

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn

import random
import json
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


with open("intents.json") as file:
    data = json.load(file)
print(data)
print(data['intents'])

words = []
labels = []
doc_x = []
doc_y=[]

for intent in data['intents']:
    for pattern in intent['patterns']:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        doc_x.append(wrds)
        doc_y.append(intent['tag'])
    
    if intent['tag'] not in labels:
        labels.append(intent['tag'])

print(words)

words = [ps.stem(w.lower()) for w in words if w!= '?']
words = sorted(list(set(words)))

labels = sorted(labels)
training = []
output = []
out_empty = [0 for _ in range(len(labels))]


for x,doc in enumerate(doc_x):
    bag = []
    wrds = [ps.stem(w1) for w1 in doc]
    for w1 in words:
        if w1 in wrds:
            bag.append(1)
        else:
            bag.append(0)
    output_row = out_empty[:]
    output_row[labels.index(doc_y[x])] = 1

    training.append(bag)
    output.append(output_row)

training =np.array(training)
output = np.array(output)

tensorflownet = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(tensorflownet, 8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("modelchatbot")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [ps.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w==se:
                bag[i] = 1
    
    return np.array(bag)

def chat():
    print("Starting chat type quit to stop")
    while True:
        inp = input('You: ')
        if inp.lower() == 'quit':
            break
        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
        print(random.choice(responses))

chat()