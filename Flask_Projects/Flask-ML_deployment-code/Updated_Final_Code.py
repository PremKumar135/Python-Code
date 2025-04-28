# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer
import warnings
warnings.filterwarnings('ignore')
import pickle
from sklearn.linear_model import LogisticRegression
import argparse


def preprocessing(text):
    text = text.lower()   #lowercase string
    text = text.strip()   #remove extra whitespaces
    text = re.sub(r'[^\w\s]', '', text) #remove punc
    text = re.sub(r'\d+', '', text)  #remove the numbers
    
    # remove stopwords
    stop_words = set(stopwords.words('english')) 
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]  
    
    #Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in filtered_sentence]
    return ' '.join(lemmas)

def vectorization(text):
    #loading the vectorizer
    with open('vec.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    
    text = [text]
    X = vectorizer.transform(text)
    return X

def best_model(vector):
    #loading the best model
    with open('best_model_LR.pkl', 'rb') as f:
        clf = pickle.load(f)
    
    result = clf.predict(vector)
    return result

def main(df):
    temp =df.copy()
    df['data'] = df.apply(lambda row: preprocessing(row['data']), axis=1)
    df['data'] = df.apply(lambda row: vectorization(row['data']), axis=1)
    df['label'] = df.apply(lambda row: int(best_model(row['data'])[0]), axis=1)
    df['data'] = temp['data']
    print('\n')
#     print('Percentage of Positive Feedback :{0}%'.format(round( (sum(list(df['label']))/(len(list(df['label']))))*100, 2)))
#     print('Percentage of Negative Feedback :{0}%'.format(round( (100 - (sum(list(df['label']))/(len(list(df['label']))))*100), 2)))
#     print('\n')
    print('INFO: All Done!!! Result is saved in "result.csv" check it out!')
    df.to_csv('result.csv')
    
if __name__=='__main__':
    inp = int(input('Enter the number of feedbacks u wanted to give :'))
    feedback = {'data': []} 
    for i in range(1,inp+1):
        feedback['data'].append(str(input(f'Enter the number {i} feedback: ')))
        
    df = pd.DataFrame(feedback)
    main(df)
    
    