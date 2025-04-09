import streamlit as st
import pandas as pd
from preprocessing.deteksi_spam import deteksi_spam


# Streamlit UI
st.title("📧 Deteksi Spam Email")

# Pilihan mode input
mode = st.radio("Pilih mode input:", ["Deteksi Satu Email", "Deteksi Banyak Email (CSV)"])

if mode == "Deteksi Satu Email":
    # Input untuk satu teks
    st.subheader("Deteksi untuk Satu Email")
    input_email = st.text_area("Masukkan isi email:")

    if st.button("Deteksi"):
        hasil = deteksi_spam(input_email)
        st.success(f"Hasil Deteksi: {hasil}")

elif mode == "Deteksi Banyak Email (CSV)":
    # Input untuk file CSV
    st.subheader("Deteksi untuk Banyak Email (CSV)")
    uploaded_file = st.file_uploader("Unggah file CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            # Membaca file CSV
            df = pd.read_csv(uploaded_file)
            st.write("Data yang diunggah:")
            st.dataframe(df.head())

            # Mengubah nama kolom menjadi huruf kecil
            df.columns = df.columns.str.lower()

            # Memastikan kolom teks ada
            text_column = st.text_input("Masukkan nama kolom yang berisi teks email:", value="email").lower()

            if text_column in df.columns:
                # Menyiapkan progress bar dan spinner
                with st.spinner("Sedang memproses..."):
                    progress_bar = st.progress(0)
                    total_rows = len(df)
                    processed_rows = 0

                    # Proses deteksi spam
                    hasil_deteksi = []
                    for teks in df[text_column]:
                        hasil_deteksi.append(deteksi_spam(teks))
                        processed_rows += 1
                        progress_bar.progress(processed_rows / total_rows)

                    # Menambahkan hasil deteksi ke DataFrame
                    df['Hasil Deteksi'] = hasil_deteksi

                # Tampilkan hasil dan tombol unduh setelah selesai
                st.success("✅ Proses deteksi selesai!")

                st.write("📄 Hasil Deteksi:")
                st.dataframe(df[[text_column, 'Hasil Deteksi']])

                # Unduh hasil
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Unduh Hasil Deteksi",
                    data=csv,
                    file_name="hasil_deteksi_spam.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"❌ Kolom '{text_column}' tidak ditemukan dalam file CSV.")
        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan saat memproses file: {e}")