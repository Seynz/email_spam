import streamlit as st
import joblib
import nltk
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
import langdetect

# Load model dan vectorizer
model = joblib.load('./model_svm_spam.pkl')
vectorizer = joblib.load('./vectorizer_tfidf.pkl')
# Siapkan tools preprocessing
stop_words = set(stopwords.words('indonesian'))
regex = re.compile(r'[\d' + string.punctuation + ']')
factory = StemmerFactory()
stemmer = factory.create_stemmer()

def preprocess_text(text):
    try:
        if langdetect.detect(text) != 'id':
            return ''
    except:
        return ''
    text = text.lower()
    text = regex.sub(' ', text)
    words = text.split()
    words = [word for word in words if word not in stop_words]
    text = ' '.join(words)
    text = stemmer.stem(text)
    return text

def deteksi_spam(teks_email):
    teks_bersih = preprocess_text(teks_email)
    teks_vector = vectorizer.transform([teks_bersih])
    hasil = model.predict(teks_vector)
    return "Spam" if hasil[0] == 0 else "Bukan Spam"

# Streamlit UI
st.title("📧 Deteksi Spam Email")
input_email = st.text_area("Masukkan isi email:")

if st.button("Deteksi"):
    hasil = deteksi_spam(input_email)
    st.success(f"Hasil Deteksi: {hasil}")
