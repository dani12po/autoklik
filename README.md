# Otomatisasi Klik Python

Skrip Python ini dirancang untuk melakukan serangkaian klik otomatis pada layar komputer Anda. Berikut adalah penjelasan tentang cara kerjanya dan apa yang perlu diinstal agar skrip ini dapat dijalankan:

## Cara Kerja Skrip

1.  **Mengimpor Library:**

    * `pyautogui`: Digunakan untuk mengontrol mouse dan keyboard.

    * `time`: Digunakan untuk mengatur waktu tunggu (delay).

    * `math`: Digunakan untuk perhitungan matematika (dalam kasus ini, menghitung jarak).

    * `re`: Digunakan untuk Regular Expression (pencarian teks).

    * `pytesseract`: Library OCR (Optical Character Recognition) untuk membaca teks dari gambar.

2.  **Konfigurasi Tesseract:**

    * Skrip mencoba mengkonfigurasi path ke Tesseract OCR. Tesseract adalah program yang digunakan untuk mengenali teks dalam gambar. Path ini mungkin berbeda tergantung pada sistem operasi dan bagaimana Tesseract diinstal.

    * Jika Tesseract tidak ditemukan, skrip akan menampilkan pesan error dan berhenti.

3.  **Fungsi `cari_gambar(nama_file, confidence=0.8)`:**

    * Fungsi ini mencari gambar tertentu di layar.

    * `nama_file` adalah nama file gambar yang ingin dicari.

    * `confidence` adalah tingkat kepercayaan (antara 0 dan 1) yang dibutuhkan agar pencarian dianggap berhasil. Nilai yang lebih tinggi berarti pencarian harus lebih akurat.

    * Jika gambar ditemukan, fungsi mengembalikan koordinat tengah gambar. Jika tidak, fungsi mengembalikan `None`.

4.  **Fungsi `hitung_jarak(p1, p2)`:**

    * Fungsi ini menghitung jarak antara dua titik di layar menggunakan rumus Euclidean.

5.  **Fungsi `auto_klik_urutan_dengan_delay_spesifik_berulang_dengan_timer_tambahan_screenshot()`:**

    * Ini adalah fungsi utama yang menjalankan logika auto-klik.

    * `koordinat_angka_statis`: Dictionary yang berisi koordinat tetap untuk angka-angka yang akan diklik.

    * `urutan_klik_awal`: List yang menentukan urutan klik angka.

    * `delay_sebelum` dan `delay_sesudah`: Dictionary yang menentukan delay sebelum dan sesudah setiap klik.

    * `default_delay`: Delay default jika tidak ada delay spesifik yang ditentukan.

    * `timer_interval`: Interval waktu (dalam detik) untuk melakukan tindakan timer (klik koordinat tambahan).

    * `gagal_3_dalam_urutan` dan `gagal_6_dalam_urutan`: Flags untuk menandai kegagalan pencarian angka 3 dan 6.

    * `siklus_berhasil`: Flag untuk menandai keberhasilan siklus klik.

    * `koordinat_klik_jika_3_tidak_muncul` dan `koordinat_klik_jika_6_tidak_muncul`: Koordinat yang akan diklik jika angka 3 atau 6 tidak ditemukan setelah timeout.

    * `timeout_3` dan `timeout_6`: Waktu timeout (dalam detik) untuk pencarian angka 3 dan 6.

    * `waktu_mulai_pencarian_3`, `waktu_mulai_pencarian_6`, `waktu_penundaan_3_berakhir`, dan `waktu_penundaan_6_berakhir`: Variabel-variabel waktu untuk mengelola timeout dan penundaan.

    * `penundaan_3_sedang_berlangsung` dan `penundaan_6_sedang_berlangsung`: Flags untuk menandai apakah penundaan sedang aktif.

    * `durasi_penundaan`: Durasi penundaan setelah klik koordinat timeout.

    * Skrip melakukan klik pada angka-angka dalam urutan yang ditentukan, dengan delay yang telah diatur.

    * Skrip mencari gambar angka 3 dan 6. Jika tidak ditemukan dalam waktu tertentu, skrip akan mengklik koordinat alternatif dan menunda klik angka-angka lain selama 20 detik.

    * Skrip juga memiliki timer yang setiap 10 menit akan melakukan klik pada koordinat tambahan.

    * Skrip mengambil screenshot untuk membantu debugging.

## Yang Perlu Diinstal

Berikut adalah langkah-langkah dan perangkat lunak yang perlu diinstal agar skrip ini dapat berjalan:

1.  **Python:**

    * Unduh dan instal Python dari <https://www.python.org/downloads/>.

    * Pastikan untuk mencentang opsi "Add Python to PATH" saat instalasi.

2.  **PyAutoGUI:**

    * Buka command prompt atau terminal.

    * Jalankan perintah: `pip install pyautogui`

3.  **PyTesseract dan Tesseract OCR:**

    * **Tesseract OCR:**

        * Unduh dan instal Tesseract OCR dari <https://tesseract-ocr.github.io/tessdoc/Home.html>.

        * Pilih versi yang sesuai dengan sistem operasi Anda.

    * **PyTesseract:**

        * Buka command prompt atau terminal.

        * Jalankan perintah: `pip install pytesseract`

    * **Konfigurasi Tesseract Path:**

        * Setelah menginstal Tesseract OCR, Anda perlu mengatur path ke executable Tesseract di dalam skrip Python.

        * Ubah baris ini dalam skrip:

            ```
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Contoh Windows
            # Atau contoh macOS/Linux:
            # pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
            ```

        * Ganti path di atas dengan path yang benar ke `tesseract.exe` di sistem Anda.

        * **Penting:** Jika path Tesseract tidak dikonfigurasi dengan benar, skrip tidak akan dapat membaca teks dari gambar.

4.  **File Gambar:**

    * Pastikan file gambar `angka_3.png` dan `angka_6.png` ada di direktori yang sama dengan skrip Python. Skrip mencari file-file ini untuk menemukan angka 3 dan 6 di layar.

## Cara Menjalankan Skrip

1.  Simpan skrip Python sebagai file `.py` (misalnya, `auto_klik.py`).

2.  Pastikan semua dependensi (Python, PyAutoGUI, PyTesseract, Tesseract OCR) sudah terinstal dan Tesseract path sudah dikonfigurasi dengan benar.

3.  Pastikan file gambar yang dibutuhkan ada di direktori yang sama dengan skrip.

4.  Buka command prompt atau terminal, arahkan ke direktori tempat Anda menyimpan skrip, dan jalankan dengan perintah: `python auto_klik.py`

## Catatan Tambahan

* Skrip ini mungkin perlu dimodifikasi agar sesuai dengan resolusi layar dan tata letak spesifik aplikasi yang Anda gunakan. Koordinat klik dan nama file gambar mungkin perlu disesuaikan.

* Gunakan skrip ini dengan hati-hati dan bertanggung jawab. Auto-klik yang berlebihan atau tidak tepat dapat menyebabkan masalah pada aplikasi atau sistem Anda.

* Skrip ini mengambil screenshot. Pastikan Anda memahami implikasinya terhadap privasi dan keamanan data Anda.
