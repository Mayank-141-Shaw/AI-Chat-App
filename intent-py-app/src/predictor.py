import os
from tabnanny import verbose
#import nltk
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import pickle

#import random
import json

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# load response data

with open( os.path.dirname(__file__) + '/intents.json') as file:
    data = json.load(file)

# load tokenizer object
with open(os.path.dirname(__file__) + './modelV3/tokenizer.pkl', 'rb') as handle:
    tokenizer = pickle.load(handle)

# load label encoder object
with open(os.path.dirname(__file__) + './modelV3/label_encoder.pkl', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# load trained model
model = keras.models.load_model(os.path.dirname(__file__) + "./modelV3/chat_model")




# parameters
max_len = 20

#with open( os.path.dirname(__file__) + '\collator_model.joblib', 'rb') as file_handler:
    #model = load(file_handler)

# prepare responses
# words = []
# labels = []
# doc_x = []
# doc_y=[]

# for intent in data['intents']:
#     for pattern in intent['patterns']:
#         wrds = nltk.word_tokenize(pattern)
#         words.extend(wrds)
#         doc_x.append(wrds)
#         doc_y.append(intent['tag'])
    
#     if intent['tag'] not in labels:
#         labels.append(intent['tag'])


# words = [ps.stem(w.lower()) for w in words if w!= '?']
# words = sorted(list(set(words)))

# labels = sorted(labels)
# training = []
# output = []
# out_empty = [0 for _ in range(len(labels))]


# for x,doc in enumerate(doc_x):
#     bag = []
#     wrds = [ps.stem(w1) for w1 in doc]
#     for w1 in words:
#         if w1 in wrds:
#             bag.append(1)
#         else:
#             bag.append(0)
#     output_row = out_empty[:]
#     output_row[labels.index(doc_y[x])] = 1

#     training.append(bag)
#     output.append(output_row)


# training =np.array(training)
# output = np.array(output)






# def get_model():
#     import tflearn
#     import tensorflow as tf

#     from tensorflow.python.framework import ops
#     ops.reset_default_graph()

#     with tf.Session() as sess:
#         new_saver = tf.train.import_meta_graph('./my_model/chatbot_model.meta')
#         new_saver.restore(sess, tf.train.latest_checkpoint('./my_model/'))
#         print(sess.run('w1:0'))

    # tensorflownet = tflearn.input_data(shape=[None, len(training[0])])
    # net = tflearn.fully_connected(tensorflownet, 8)
    # net = tflearn.fully_connected(net,8)
    # net = tflearn.fully_connected(net, len(output[0]), activation='softmax')
    # net = tflearn.regression(net)

    # model = tflearn.DNN(net)
    # model.load('./my_model/')
    # # load computed model
    # with open(os.path.dirname(__file__) +'./my_model/chatbot_model', 'rb') as file_handler:
    #     model.load(file_handler)

    # return model






# def bag_of_words(s, words):
#     bag = [0 for _ in range(len(words))]
#     s_words = nltk.word_tokenize(s)
#     s_words = [ps.stem(word.lower()) for word in s_words]
    
#     for se in s_words:
#         for i, w in enumerate(words):
#             if w==se:
#                 bag[i] = 1
#     print(np.array(bag))
#     return np.array(bag)





def predict(inp_msg):
    res = 'No result'

    results = model.predict(
                    keras
                    .preprocessing
                    .sequence
                    .pad_sequences(
                        tokenizer
                        .texts_to_sequences(
                                    [inp_msg]),
                                    truncating='post', 
                                    maxlen=max_len
                                )
                            )

    tag = lbl_encoder.inverse_transform([np.argmax(results)])

    for i in data['intents']:
        if i['tag'] == tag:
            res = np.random.choice(i['responses'])
            break
    
    return res

    # results = model.predict([bag_of_words(inp_msg, words)])      # here is the problem in the model check it 
    
    # #results = model.predict([[10, 20, 30]])
    # print(results)

    # results_index = np.argmax(results)
    # tag = labels[results_index]

    # for tg in data['intents']:
    #     if tg['tag'] == tag:
    #         responses = tg['responses']
    # res = random.choice(responses)
    # print(res)
    # return res


if __name__ == '__main__':
    print(predict('hello'))