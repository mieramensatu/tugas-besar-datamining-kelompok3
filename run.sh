#!/bin/bash

echo " Menjalankan pipeline Analisis Klaster Toko Erigo..."

# Optional: Cek dan install requirements
if [ -f requirements.txt ]; then
    echo " Menginstall dependensi dari requirements.txt..."
    pip install -r requirements.txt
    playwright install
fi

# Jalankan pipeline utama
echo " Menjalankan notebook/main.ipynb..."
jupyter notebook notebook/main.ipynb