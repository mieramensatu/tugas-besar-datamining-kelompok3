# 📊 ANALISIS KLASTER PELANGGAN TOKO ONLINE  
**Studi Kasus: Toko Erigo di Tokopedia**

Repositori ini berisi proyek data mining untuk melakukan klasterisasi pelanggan dari Toko Erigo di Tokopedia, menggunakan metode K-Means dan eksplorasi data berbasis Python.

---

### 🗂 Struktur Direktori

```
erigo_clustering/
│
├── data/
│   ├── raw/
│   │   └── Erigo_full_data.csv            # Dataset hasil scraping dari Tokopedia
│   └── processed/
│       └── cleaned_tokped_data.csv        # Dataset setelah preprocessing
│
├── notebook/
│   ├── EDA.ipynb                          # Eksplorasi data (EDA)
│   ├── Evaluasi.ipynb                     # Evaluasi model klaster
│   ├── Modeling.ipynb                     # Klasterisasi dengan K-Means
│   └── Processing.ipynb                   # Preprocessing data mentah
│
├── report/
│   ├── Laporan Akhir Kasus 3.docx         # Laporan akhir proyek
│   └── Laporan Akhir Kasus 3.pdf          # Laporan akhir proyek
│
├── src/
│   ├── main.ipynb                         # Notebook ringkasan pipeline
│   └── scrapping.py                       # Script scraping data Tokopedia
│
├── README.md                              # Dokumentasi utama proyek
├── requirements.txt                       # Daftar dependensi Python
└── run.sh                                 # Script bash untuk menjalankan pipeline
```

---

## 🚀 Cara Menjalankan

### ✅ 1. Persiapkan Environment

Install pustaka yang dibutuhkan:

```bash
pip install -r requirements.txt
```

Untuk scraping data:

```bash
playwright install
```

### ✅ 2. Jalankan Proyek

#### 💻 Jalankan Scraping (opsional):

```bash
python src/scrapping.py
```

#### 📒 Jalankan Analisis via Jupyter Notebook:

Urutan notebook yang disarankan:

```text
1. notebook/Processing.ipynb
2. notebook/EDA.ipynb
3. notebook/Modeling.ipynb
4. notebook/Evaluasi.ipynb
5. src/main.ipynb (ringkasan pipeline)
```

---

## 📦 Struktur Modular

- **`scrapping.py`**: Mengambil data toko dan produk dari Tokopedia menggunakan Playwright.
- **`Processing.ipynb`**: Membersihkan dan menyiapkan data untuk klasterisasi.
- **`EDA.ipynb`**: Menjelajahi pola awal dan distribusi data.
- **`Modeling.ipynb`**: Klasterisasi pelanggan dengan algoritma K-Means.
- **`Evaluasi.ipynb`**: Menilai kualitas klaster menggunakan Elbow & Silhouette.
- **`main.ipynb`**: Notebook all-in-one untuk menjalankan semua tahapan sekaligus.

---

## 📈 Evaluasi & Hasil

- **Jumlah klaster optimal**: 3 (berdasarkan Elbow & Silhouette Score)
- **Ciri Klaster**:
  - Klaster 0: Produk murah & populer
  - Klaster 1: Produk menengah & stabil
  - Klaster 2: Produk mahal dengan ulasan terbatas

---

## 📓 Catatan

- File `Erigo_full_data.csv` adalah output dari proses scraping
- Dataset hasil preprocessing: `cleaned_tokped_data.csv`
- Jika ingin memperbarui data, jalankan `scrapping.py`

---

## 👥 Anggota Kelompok

- Gading Khairlambang – 714220007  
- Ahmad Rifki Ayala – 714220028  
- Nayaka Taqwa – 714220045  

---

## 📄 Lisensi

Proyek ini dibuat untuk tujuan edukasi dalam mata kuliah *Data Mining*. Bebas digunakan untuk pembelajaran dan referensi akademik.
