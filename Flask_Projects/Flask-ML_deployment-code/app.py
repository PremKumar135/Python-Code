import numpy as np
import pandas as pd
import pickle
from flask import Flask, jsonify, render_template, request
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
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
    vectorizer = pickle.load(open('vec.pkl', 'rb'))
    text = [text]
    X = vectorizer.transform(text)
    return X

#model
def predict_vec(vector):
    model = pickle.load(open('best_model_LR.pkl', 'rb'))
    result = model.predict(vector)
    return result

@app.route('/predict', methods=['POST'])
def predict():
    json_ = request.json
    query_df = pd.DataFrame(json_)
    query_df['Review'] = query_df.apply(lambda row: preprocessing(row['Review']), axis=1)
    query_df['vector'] = query_df.apply(lambda row:vectorization(row['Review']), axis=1)
    query_df['pred'] = query_df.apply(lambda row:predict_vec(row['vector']),axis=1)
    prediction = [i[0] for i in query_df['pred']]
    return jsonify({'prediction':prediction})
    
if __name__=='__main__':
        app.run(debug=True)