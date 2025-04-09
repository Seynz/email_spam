
# 📧 Deteksi Spam Email Bahasa Indonesia

Aplikasi Streamlit sederhana untuk mendeteksi apakah email dalam bahasa Indonesia termasuk **spam** atau **bukan spam**, menggunakan model SVM yang sudah dilatih sebelumnya.

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Instalasi Dependensi
Pastikan kamu sudah meng-install semua library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

### 2. Unduh Resource Tambahan untuk NLTK
Jalankan skrip berikut untuk mengunduh data yang dibutuhkan oleh NLTK:

```bash
python setup_nltk.py
```

### 3. Jalankan Aplikasi Streamlit

```bash
streamlit run app.py
```

---

## 📁 Struktur Direktori

```
.
├── data/
│   ├── data_dummy_raw.csv
│   └── teks_percobaan.txt
├── model/
│   ├── model_svm_spam.pkl
│   └── vectorizer_tfidf.pkl
├── preprocessing/
│   └── spam_detector.py
├── app.py
├── requirements.txt
├── setup_nltk.py
└── README.md
```

---

## 📦 Dataset

Dataset yang digunakan untuk pelatihan model tersedia di Kaggle:  
🔗 [Indonesian Email Spam Dataset](https://www.kaggle.com/datasets/gevabriel/indonesian-email-spam)

---

## 🧠 Teknologi yang Digunakan

- Python
- Scikit-learn
- NLTK
- Sastrawi (untuk stemming Bahasa Indonesia)
- Streamlit (untuk UI interaktif)
