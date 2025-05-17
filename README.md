# Auto Clicker dengan Pencarian Gambar dan Timer

Skrip Python ini melakukan auto klik pada urutan angka di layar, dengan penanganan khusus untuk angka 3 dan 6 yang dicari menggunakan pencocokan gambar. Skrip ini juga memiliki fitur timer untuk melakukan klik pada koordinat tambahan setiap 10 menit.

## Prasyarat

Sebelum menjalankan skrip ini, Anda perlu menginstal beberapa perangkat lunak dan library Python:

1.  **Python 3:** Pastikan Anda telah menginstal Python 3 di sistem Anda. Anda dapat mengunduhnya dari situs web resmi Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2.  **Tesseract OCR:** Skrip ini menggunakan Tesseract Optical Character Recognition (OCR) untuk mencari teks pada gambar (meskipun dalam skrip ini lebih fokus pada pencarian gambar). Anda perlu menginstal Tesseract OCR dan memastikan path-nya dikonfigurasi dengan benar dalam skrip.

    * **Windows:**
        * Unduh installer dari [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki). Pilih versi yang sesuai dengan sistem Anda (misalnya, `tesseract-ocr-w64-setup-5.x.xxxx.exe`).
        * Setelah instalasi, cari direktori instalasi Tesseract (biasanya di `C:\Program Files\Tesseract-OCR\`). Anda akan membutuhkan path ini untuk konfigurasi skrip.

    * **macOS:**
        * Anda dapat menginstal Tesseract menggunakan Homebrew. Jika Anda belum menginstal Homebrew, ikuti instruksi di [https://brew.sh/](https://brew.sh/).
        * Buka Terminal dan jalankan perintah:
            ```bash
            brew install tesseract
            ```

    * **Linux (Debian/Ubuntu):**
        * Buka Terminal dan jalankan perintah:
            ```bash
            sudo apt update
            sudo apt install tesseract-ocr
            ```
        * Untuk distribusi lain, gunakan manajer paket yang sesuai (misalnya, `yum` pada CentOS/Fedora).

3.  **Library Python:** Anda perlu menginstal library `pyautogui` dan `pytesseract`. Buka Command Prompt (Windows) atau Terminal (macOS/Linux) dan jalankan perintah:
    ```bash
    pip install pyautogui pytesseract Pillow
    ```
    * `pyautogui`: Digunakan untuk mengontrol mouse dan keyboard.
    * `pytesseract`: Sebagai wrapper untuk Tesseract OCR (meskipun dalam skrip ini lebih untuk konfigurasi path).
    * `Pillow`: Library manipulasi gambar yang dibutuhkan oleh `pyautogui`.

## Instalasi dan Konfigurasi

1.  **Simpan Skrip Python:** Simpan kode Python yang telah diberikan ke dalam sebuah file, misalnya `auto_clicker.py`.

2.  **Siapkan Gambar:** Pastikan Anda memiliki file gambar untuk angka 3 (`angka_3.png`) dan angka 6 (`angka_6.png`) yang akan dicari di layar. Letakkan file-file gambar ini di direktori yang sama dengan skrip `auto_clicker.py`.

3.  **Konfigurasi Path Tesseract (di dalam skrip):** Buka file `auto_clicker.py` dengan editor teks. Cari bagian berikut:
    ```python
    # Konfigurasikan path Tesseract (sesuaikan dengan sistem Anda)
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'   # Contoh Windows
        # Atau contoh macOS/Linux:
        # pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
        print(f"Path Tesseract yang dikonfigurasi: {pytesseract.pytesseract.tesseract_cmd}")
    except pytesseract.TesseractNotFoundError as e:
        print(f"Error: Tesseract tidak ditemukan. Pastikan terinstal dan path dikonfigurasi dengan benar.\n{e}")
        exit()
    ```
    * **Windows:** Ganti `r'C:\Program Files\Tesseract-OCR\tesseract.exe'` dengan path sebenarnya ke file `tesseract.exe` di sistem Anda. Contoh umumnya adalah `C:\Program Files\Tesseract-OCR\tesseract.exe` atau `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`.
    * **macOS:** Jika Anda menginstal Tesseract menggunakan Homebrew, path biasanya adalah `/usr/local/bin/tesseract`. Uncomment baris yang sesuai dan sesuaikan jika perlu.
    * **Linux:** Biasanya, Tesseract akan berada di dalam system PATH, jadi Anda mungkin tidak perlu mengubah baris ini.

## Mengatur Posisi Klik yang Diinginkan

Skrip ini saat ini dikonfigurasi dengan koordinat statis untuk angka 1, 2, 4, dan 5. Untuk mengatur posisi klik yang sesuai dengan tata letak di layar Anda, Anda perlu memodifikasi koordinat ini di dalam skrip `auto_clicker.py`. Berikut caranya:

1.  **Gunakan `pyautogui.position()` untuk Mendapatkan Koordinat:**
    * Anda dapat menggunakan fungsi `pyautogui.position()` untuk mengetahui posisi kursor mouse saat ini di layar.
    * Buka Command Prompt (Windows) atau Terminal (macOS/Linux) dan jalankan interpreter Python interaktif:
      ```bash
      python
      ```
    * Impor library `pyautogui`:
      ```python
      import pyautogui
      ```
    * Pindahkan kursor mouse ke posisi angka yang ingin Anda klik di layar Anda, lalu jalankan perintah berikut di interpreter Python:
      ```python
      pyautogui.position()
      ```
    * Ini akan mengembalikan tuple yang berisi koordinat x dan y dari posisi kursor saat itu, misalnya `Point(x=918, y=804)`. Catat nilai-nilai ini.

2.  **Modifikasi Koordinat dalam Skrip:**
    * Buka kembali file `auto_clicker.py` dengan editor teks.
    * Cari bagian `koordinat_angka_statis`:
      ```python
      koordinat_angka_statis = {
          1: (918, 804),
          2: (911, 1073),
          4: (1759, 809),
          5: (1748, 1073),
      }
      ```
    * Ganti nilai-nilai koordinat yang ada dengan koordinat yang Anda dapatkan pada langkah sebelumnya untuk angka 1, 2, 4, dan 5 sesuai dengan posisi di layar Anda. Misalnya, jika posisi angka 1 di layar Anda adalah (100, 200), ubah barisnya menjadi:
      ```python
      1: (100, 200),
      ```
    * Lakukan hal yang sama untuk angka 2, 4, dan 5.

3.  **Koordinat Fallback untuk Angka 3 dan 6:**
    * Skrip juga memiliki koordinat fallback yang digunakan jika gambar angka 3 atau 6 tidak ditemukan setelah timeout:
      ```python
      koordinat_klik_jika_3_tidak_muncul = (96, 65)
      koordinat_klik_jika_6_tidak_muncul = (1055, 64)
      ```
    * Anda juga dapat menggunakan metode `pyautogui.position()` untuk mendapatkan koordinat fallback yang sesuai jika diperlukan dan mengganti nilai-nilai ini.

4.  **Simpan Perubahan:** Setelah memodifikasi koordinat, simpan perubahan pada file `auto_clicker.py`.

Dengan mengikuti langkah-langkah ini, Anda dapat menyesuaikan posisi klik dalam skrip agar sesuai dengan tata letak angka di layar Anda.

## Penggunaan

1.  **Buka Tab Target:** Pastikan tab atau jendela aplikasi yang ingin Anda targetkan untuk auto klik aktif dan terlihat di layar Anda.

2.  **Jalankan Skrip:** Buka Command Prompt (Windows) atau Terminal (macOS/Linux), navigasikan ke direktori tempat Anda menyimpan `auto_clicker.py`, dan jalankan skrip menggunakan perintah:
    ```bash
    python auto_clicker.py
    ```

3.  **Ikuti Instruksi:** Skrip akan mencetak instruksi di konsol. Anda perlu memastikan tab target aktif dan kemudian menekan Enter untuk memulai proses auto klik.

4.  **Proses Auto Klik:**
    * Skrip akan pertama-tama melakukan klik pada koordinat statis untuk angka 1 (sesuai dengan konfigurasi Anda).
    * Kemudian, skrip akan berulang kali mencoba mengklik urutan angka 2, 3, 6, 4, dan 5 (dengan koordinat statis yang telah Anda atur).
    * Untuk angka 3 dan 6, skrip akan mencari gambar `angka_3.png` dan `angka_6.png` di layar.
    * Jika angka 3 atau 6 tidak ditemukan dalam waktu tertentu (timeout 2 menit), skrip akan melakukan klik pada koordinat fallback yang telah Anda konfigurasi dan menunda klik angka-angka tertentu selama 20 detik.
    * Setiap 10 menit, skrip akan melakukan klik pada koordinat tambahan (saat ini (101, 60) dan (1055, 64), Anda juga dapat menyesuaikannya).
    * Screenshot akan diambil sebelum dan sesudah pencarian gambar angka 3 dan 6, dan disimpan di direktori yang sama dengan skrip.

5.  **Menghentikan Skrip:** Untuk menghentikan skrip kapan saja, tekan `Ctrl+C` di jendela Command Prompt atau Terminal.

## Catatan Penting

* **Koordinat Statis:** Pastikan koordinat statis untuk angka 1, 2, 4, dan 5 telah Anda atur dengan benar sesuai posisi di layar Anda.
* **Pencocokan Gambar:** Keberhasilan pencarian gambar sangat bergantung pada kualitas gambar `angka_3.png` dan `angka_6.png` serta tampilan di layar Anda. Pastikan gambar akurat dan tidak terhalang. Parameter `confidence` dalam fungsi `cari_gambar` dapat disesuaikan jika diperlukan.
* **Timeout dan Penundaan:** Nilai timeout (untuk pencarian angka 3 dan 6) dan durasi penundaan (setelah kegagalan) dapat disesuaikan dalam skrip sesuai kebutuhan Anda.
* **Timer:** Interval timer (saat ini 10 menit) dan koordinat klik timer (saat ini (101, 60) dan (1055, 64)) juga dapat diubah sesuai kebutuhan.
* **Path Tesseract:** Pastikan path Tesseract dikonfigurasi dengan benar agar tidak terjadi error. Meskipun skrip ini tidak secara intensif menggunakan OCR, library `pytesseract` mungkin membutuhkannya untuk inisialisasi.

Pastikan Anda memahami cara kerja skrip dan risiko yang mungkin timbul sebelum menjalankannya. Gunakan dengan hati-hati dan bertanggung jawab.
