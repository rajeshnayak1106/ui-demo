import streamlit as st
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation

# Load model and preprocessing tools
model = load_model("sentiment_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Preprocessing function
def preprocess(text):
    lemm = WordNetLemmatizer()
    text = re.sub(r"@+[a-zA-Z]+", " ", text)
    text = re.sub(r"[^a-zA-Z]", " ", text)
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in punctuation and t not in stopwords.words("english")]
    lemmatized = [lemm.lemmatize(t) for t in tokens]
    return " ".join(lemmatized)

# Streamlit UI
st.title("Tweet Sentiment Classifier")

user_input = st.text_area("Enter a tweet:")
if st.button("Classify"):
    processed = preprocess(user_input)
    sequence = tokenizer.texts_to_sequences([processed])
    padded = pad_sequences(sequence, maxlen=model.input_shape[1])
    pred = np.argmax(model.predict(padded), axis=1)
    sentiment = label_encoder.inverse_transform(pred)
    st.success(f"Predicted Sentiment: {sentiment[0]}")
