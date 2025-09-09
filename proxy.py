# File: proxy.py
# Deskripsi: Server proxy sederhana menggunakan Python dan Flask.

from flask import Flask, request, Response
from flask_cors import CORS
import requests

# Inisialisasi aplikasi Flask
app = Flask(__name__)
# Aktifkan CORS untuk semua domain di aplikasi ini
CORS(app)

# Alamat dasar API Deezer
DEEZER_API_URL = "https://api.deezer.com"

# Definisikan rute yang akan menangkap semua permintaan
# Contoh: Jika ada permintaan ke /chart, variabel 'path' akan berisi 'chart'
@app.route('/<path:path>', methods=['GET'])
def proxy(path):
    """
    Fungsi ini akan menerima permintaan, meneruskannya ke Deezer,
    dan mengembalikan respons dari Deezer ke browser Anda.
    """
    # Gabungkan dengan URL Deezer dan tambahkan query string jika ada
    # (misalnya ?q=eminem atau ?limit=50)
    full_url = f"{DEEZER_API_URL}/{path}?{request.query_string.decode('utf-8')}"

    try:
        # Gunakan library requests untuk mengambil data dari URL Deezer
        response = requests.get(full_url)
        
        # Buat respons baru untuk dikirim kembali ke browser Anda
        # dengan konten, status, dan tipe konten yang sama seperti dari Deezer
        proxied_response = Response(
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type']
        )
        
        return proxied_response

    except requests.exceptions.RequestException as e:
        # Jika terjadi error saat menghubungi Deezer
        print(f"Error contacting Deezer API: {e}")
        return "Gagal menghubungi API Deezer", 500

# Jalankan server jika file ini dieksekusi secara langsung
if __name__ == '__main__':
    # Server akan berjalan di port 8084
    app.run(port=8084)

