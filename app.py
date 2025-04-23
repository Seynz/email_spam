# Import library yang dibutuhkan
import streamlit as st  # Untuk membuat UI berbasis web
import pandas as pd  # Untuk manipulasi data
from preprocessing.deteksi_spam import deteksi_spam  # Fungsi deteksi spam yang sudah dibuat
import io  # Untuk operasi input/output byte (digunakan saat download file)

# Judul aplikasi Streamlit
st.title("📧 Deteksi Spam Email")

# Pilihan mode input: satu email atau banyak email via CSV
mode = st.radio("Pilih mode input:", ["Deteksi Satu Email", "Deteksi Banyak Email (CSV)"])

# Mode untuk deteksi satu email
if mode == "Deteksi Satu Email":
    st.subheader("Deteksi untuk Satu Email")  # Subjudul
    input_email = st.text_area("Masukkan isi email:")  # Input teks email dari user

    # Tombol untuk memulai proses deteksi
    if st.button("Deteksi"):
        hasil = deteksi_spam(input_email)  # Panggil fungsi deteksi spam
        st.success(f"Hasil Deteksi: {hasil}")  # Tampilkan hasil

# Mode untuk deteksi banyak email dari file CSV
elif mode == "Deteksi Banyak Email (CSV)":
    st.subheader("Deteksi untuk Banyak Email (CSV)")  # Subjudul
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])  # Upload file CSV

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)  # Membaca file CSV ke DataFrame
            st.write("Data yang diunggah:")
            st.dataframe(df.head())  # Menampilkan preview data

            df.columns = df.columns.str.lower()  # Konversi semua nama kolom ke huruf kecil

            # Input nama kolom yang berisi teks email, default 'email'
            text_column = st.text_input("Masukkan nama kolom yang berisi teks email:", value="email").lower()

            if text_column in df.columns:
                with st.spinner("Sedang memproses..."):  # Menampilkan spinner saat proses berjalan
                    progress_bar = st.progress(0)  # Inisialisasi progress bar
                    total_rows = len(df)  # Total baris data
                    processed_rows = 0  # Jumlah baris yang telah diproses

                    hasil_deteksi = []  # Menyimpan hasil deteksi spam

                    # Iterasi setiap baris teks email untuk dideteksi
                    for teks in df[text_column]:
                        hasil_deteksi.append(deteksi_spam(teks))  # Deteksi spam untuk setiap teks
                        processed_rows += 1
                        progress_bar.progress(processed_rows / total_rows)  # Update progress bar

                    df['Hasil Deteksi'] = hasil_deteksi  # Tambahkan hasil ke DataFrame

                st.success("✅ Proses deteksi selesai!")  # Notifikasi selesai

                st.write("📄 Hasil Deteksi:")
                st.dataframe(df[[text_column, 'Hasil Deteksi']])  # Tampilkan hasil deteksi

                # Persiapan file hasil dalam format Excel untuk diunduh
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Hasil')

                # Tombol untuk mengunduh hasil
                st.download_button(
                    label="⬇️ Unduh Hasil Deteksi",
                    data=output.getvalue(),
                    file_name="hasil_deteksi_spam.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                # Tampilkan error jika nama kolom tidak ditemukan
                st.error(f"❌ Kolom '{text_column}' tidak ditemukan dalam file CSV.")
        except Exception as e:
            # Tangani dan tampilkan error jika proses gagal
            st.error(f"⚠️ Terjadi kesalahan saat memproses file: {e}")
