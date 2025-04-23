# Import library yang dibutuhkan
import joblib  # Untuk load model dan vectorizer yang telah disimpan
import nltk  # Natural Language Toolkit, digunakan untuk stopwords
import re  # Untuk pemrosesan regular expression
import string  # Untuk memproses karakter tanda baca
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  # Untuk stemming bahasa Indonesia
from nltk.corpus import stopwords  # Untuk mengambil daftar stopword
import langdetect  # Untuk mendeteksi bahasa dari teks

# Load model klasifikasi SVM dan vectorizer TF-IDF
model = joblib.load('./model/model_svm_spam.pkl')  # Load model klasifikasi yang telah dilatih
vectorizer = joblib.load('./model/vectorizer_tfidf.pkl')  # Load vectorizer TF-IDF untuk transformasi teks

# Siapkan stopwords dan tools preprocessing lainnya
stop_words = set(stopwords.words('indonesian'))  # Ambil daftar stopwords bahasa Indonesia
regex = re.compile(r'[\d' + string.punctuation + ']')  # Buat regex untuk menghapus angka dan tanda baca
factory = StemmerFactory()
stemmer = factory.create_stemmer()  # Buat objek stemmer dari Sastrawi

# Fungsi untuk preprocessing teks email
def preprocess_text(text):
    try:
        # Deteksi bahasa, hanya proses jika bahasa Indonesia
        if langdetect.detect(text) != 'id':
            return ''
    except:
        return ''
    
    text = text.lower()  # Ubah semua huruf menjadi lowercase
    text = regex.sub(' ', text)  # Hapus angka dan tanda baca
    words = text.split()  # Tokenisasi manual dengan split spasi
    words = [word for word in words if word not in stop_words]  # Hapus stopwords
    text = ' '.join(words)  # Gabungkan kembali menjadi string
    text = stemmer.stem(text)  # Lakukan stemming
    return text

# Fungsi utama untuk mendeteksi apakah email termasuk spam
def deteksi_spam(teks_email):
    teks_bersih = preprocess_text(teks_email)  # Lakukan preprocessing
    teks_vector = vectorizer.transform([teks_bersih])  # Transformasi teks ke bentuk vektor
    hasil = model.predict(teks_vector)  # Prediksi menggunakan model
    return "Spam" if hasil[0] == 0 else "Bukan Spam"  # Return label hasil prediksi
