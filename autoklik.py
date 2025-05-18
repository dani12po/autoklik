import pyautogui
import time
import math
import re
import pytesseract

# Konfigurasikan path Tesseract (sesuaikan dengan sistem Anda)
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'   # Contoh Windows
    # Atau contoh macOS/Linux:
    # pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    print(f"Path Tesseract yang dikonfigurasi: {pytesseract.pytesseract.tesseract_cmd}")
except pytesseract.TesseractNotFoundError as e:
    print(f"Error: Tesseract tidak ditemukan. Pastikan terinstal dan path dikonfigurasi dengan benar.\n{e}")
    exit()

def cari_gambar(nama_file, confidence=0.8):
    """Mencari gambar di layar dan mengembalikan koordinat tengah jika ditemukan."""
    try:
        lokasi = pyautogui.locateCenterOnScreen(nama_file, confidence=confidence)
        return lokasi
    except pyautogui.ImageNotFoundException:
        return None

def hitung_jarak(p1, p2):
    """Menghitung jarak Euclidean antara dua titik (x, y)."""
    return math.sqrt((p2["x"] - p1["x"])**2 + (p2["y"] - p1["y"])**2)

def auto_klik_urutan_dengan_prioritas_3_6_timer_screenshot_fixed():
    """
    Melakukan auto klik pada urutan angka, dengan prioritas pencarian dan klik
    pada gambar angka 3 dan 6 jika keduanya muncul di layar.
    Tetap mempertahankan logika penanganan kegagalan untuk 3 dan 6.
    Serta mengklik koordinat tambahan setiap 10 menit.
    Memulai dari nomor 1 dalam setiap siklus.
    """
    try:
        koordinat_angka_statis = {
            1: {"x": 918, "y": 804},
            2: {"x": 911, "y": 1073},
            4: {"x": 1759, "y": 809},
            5: {"x": 1748, "y": 1073},
        }

        urutan_klik = [1, 2, 3, 6, 4, 5] # Urutan klik lengkap, dimulai dari 1
        delay_sebelum = {1: 0.2, 2: 0.2, 4: 0.2, 5: 0.2}
        delay_sesudah = {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5, 5: 0.5, 6: 0.5}
        default_delay = 1
        timer_interval = 600
        last_timer_action = time.time()
        gagal_3_dalam_urutan = False
        gagal_6_dalam_urutan = False

        # Koordinat untuk klik jika angka 3 atau 6 tidak muncul setelah timeout
        koordinat_klik_jika_3_tidak_muncul = (96, 65)
        koordinat_klik_jika_6_tidak_muncul = (1055, 63)
        timeout_3 = 120   # 2 menit dalam detik
        timeout_6 = 120   # 2 menit dalam detik
        waktu_mulai_pencarian_3 = 0
        waktu_mulai_pencarian_6 = 0
        waktu_penundaan_3_berakhir = 0
        waktu_penundaan_6_berakhir = 0
        penundaan_3_sedang_berlangsung = False
        penundaan_6_sedang_berlangsung = False
        durasi_penundaan = 20

        print(f"Memulai auto klik dengan prioritas gambar 3 & 6. Urutan: {urutan_klik}. Pencarian proaktif untuk 3 & 6 dengan timeout {timeout_3} detik. Timer setiap {timer_interval // 60} menit.")

        while True:
            gagal_3_dalam_urutan = False
            gagal_6_dalam_urutan = False

            # Prioritaskan pencarian gambar 3 dan 6 di awal setiap iterasi utama
            lokasi_3_prioritas = cari_gambar("angka_3.png", confidence=0.7)
            lokasi_6_prioritas = cari_gambar("angka_6.png", confidence=0.7)

            if lokasi_3_prioritas:
                print(f"\n=== Prioritas: Angka 3 ditemukan di {lokasi_3_prioritas}. Langsung diklik. ===")
                time.sleep(default_delay)
                pyautogui.click(lokasi_3_prioritas)
                time.sleep(delay_sesudah.get(3, default_delay))
                continue # Kembali ke awal loop while untuk mencari prioritas lagi

            if lokasi_6_prioritas:
                print(f"\n=== Prioritas: Angka 6 ditemukan di {lokasi_6_prioritas}. Langsung diklik. ===")
                time.sleep(default_delay)
                pyautogui.click(lokasi_6_prioritas)
                time.sleep(delay_sesudah.get(6, default_delay))
                continue # Kembali ke awal loop while untuk mencari prioritas lagi

            # Jika tidak ada prioritas yang ditemukan, lanjutkan dengan urutan normal
            for index, angka in enumerate(urutan_klik): # Loop melalui urutan angka yang akan diklik
                berhasil_klik = False

                # Cek apakah sedang dalam masa penundaan untuk angka 1, 2, dan 3
                if (angka in [1, 2, 3]) and penundaan_3_sedang_berlangsung:
                    if time.time() < waktu_penundaan_3_berakhir:
                        print(f"Melewati angka {angka} karena penundaan 20 detik sedang berlangsung.")
                        continue   # Lewati iterasi ini, jangan klik
                    else:
                        penundaan_3_sedang_berlangsung = False   # Penundaan selesai, reset flag
                        print(f"Penundaan 20 detik untuk angka 1, 2, dan 3 selesai.")

                # Cek apakah sedang dalam masa penundaan untuk angka 4
                if (angka in [4]) and penundaan_6_sedang_berlangsung:
                    if time.time() < waktu_penundaan_6_berakhir:
                        print(f"Melewati angka {angka} karena penundaan 20 detik sedang berlangsung.")
                        continue   # Lewati iterasi ini, jangan klik
                    else:
                        penundaan_6_sedang_berlangsung = False   # Penundaan selesai, reset flag
                        print(f"Penundaan 20 detik untuk angka 4 selesai.")

                if angka in koordinat_angka_statis:
                    delay_pre = delay_sebelum.get(angka, default_delay)
                    print(f"Menunggu {delay_pre} detik sebelum klik angka {angka}...")
                    time.sleep(delay_pre)
                    x = koordinat_angka_statis.get(angka).get("x")
                    y = koordinat_angka_statis.get(angka).get("y")
                    print(f"Mengklik angka {angka} di ({x}, {y})")
                    time.sleep(default_delay)
                    pyautogui.click(x, y)
                    berhasil_klik = True
                    delay_post = delay_sesudah.get(angka, default_delay)
                    print(f"Menunggu {delay_post} detik setelah klik angka {angka}...")
                    time.sleep(delay_post)

                elif angka == 3:
                    if waktu_mulai_pencarian_3 == 0:
                        waktu_mulai_pencarian_3 = time.time()
                    print("\n=== Mencari angka 3 sesuai urutan ===")
                    pyautogui.screenshot("screenshot_before_cari_angka_3.png")
                    print("Screenshot sebelum mencari angka 3 disimpan.")
                    lokasi_3_urutan = cari_gambar("angka_3.png", confidence=0.7)
                    if lokasi_3_urutan:
                        print(f"Angka 3 ditemukan di {lokasi_3_urutan} (pencarian urutan)")
                        print(f"Mengklik angka 3 di {lokasi_3_urutan}")
                        time.sleep(default_delay)
                        pyautogui.click(lokasi_3_urutan)
                        time.sleep(delay_sesudah.get(angka, default_delay))
                        berhasil_klik = True
                        waktu_mulai_pencarian_3 = 0   # Reset timer
                    else:
                        print("Angka 3 tidak ditemukan dalam pencarian urutan.")
                        gagal_3_dalam_urutan = True
                    pyautogui.screenshot("screenshot_after_cari_angka_3.png")
                    print("Screenshot setelah mencari angka 3 disimpan.")

                elif angka == 6:
                    if waktu_mulai_pencarian_6 == 0:
                        waktu_mulai_pencarian_6 = time.time()
                    print("\n=== Mencari angka 6 sesuai urutan ===")
                    pyautogui.screenshot("screenshot_before_cari_angka_6.png")
                    print("Screenshot sebelum mencari angka 6 disimpan.")
                    lokasi_6_urutan = cari_gambar("angka_6.png", confidence=0.7)
                    if lokasi_6_urutan:
                        print(f"Angka 6 ditemukan di {lokasi_6_urutan} (pencarian urutan)")
                        print(f"Mengklik angka 6 di {lokasi_6_urutan}")
                        time.sleep(default_delay)
                        pyautogui.click(lokasi_6_urutan)
                        time.sleep(delay_sesudah.get(angka, default_delay))
                        berhasil_klik = True
                        waktu_mulai_pencarian_6 = 0   # Reset timer
                    else:
                        print("Angka 6 tidak ditemukan dalam pencarian urutan.")
                        gagal_6_dalam_urutan = True
                    pyautogui.screenshot("screenshot_after_cari_angka_6.png")
                    print("Screenshot setelah mencari angka 6 disimpan.")

                else:
                    print(f"Logika untuk angka {angka} belum diimplementasikan.")
                    break # Keluar dari loop for

                if not berhasil_klik and angka == 3:
                    if time.time() - waktu_mulai_pencarian_3 >= timeout_3:
                        print(f"Angka 3 tidak ditemukan setelah {timeout_3} detik. Mengklik koordinat {koordinat_klik_jika_3_tidak_muncul}")
                        pyautogui.click(koordinat_klik_jika_3_tidak_muncul)
                        time.sleep(default_delay)
                        waktu_mulai_pencarian_3 = 0   # Reset timer setelah klik
                        gagal_3_dalam_urutan = True   # Set flag gagal
                        penundaan_3_sedang_berlangsung = True
                        waktu_penundaan_3_berakhir = time.time() + durasi_penundaan
                        print(f"Menunda klik angka 1, 2, dan 3 selama {durasi_penundaan} detik.")
                        continue   # Lanjutkan ke iterasi berikutnya dari loop while

                if not berhasil_klik and angka == 6:
                    if time.time() - waktu_mulai_pencarian_6 >= timeout_6:
                        print(f"Angka 6 tidak ditemukan setelah {timeout_6} detik. Mengklik koordinat {koordinat_klik_jika_6_tidak_muncul}")
                        pyautogui.click(koordinat_klik_jika_6_tidak_muncul)
                        time.sleep(default_delay)
                        waktu_mulai_pencarian_6 = 0   # Reset timer setelah klik
                        gagal_6_dalam_urutan = True   # Set flag gagal
                        penundaan_6_sedang_berlangsung = True
                        waktu_penundaan_6_berakhir = time.time() + durasi_penundaan
                        print(f"Menunda klik angka 4 selama {durasi_penundaan} detik.")
                        continue   # Lanjutkan ke iterasi berikutnya dari loop while

            # Setelah menyelesaikan (atau gagal di tengah) urutan, loop akan berlanjut
            # ke awal loop while untuk memulai urutan dari angka 1 lagi.

            elapsed_time_timer = time.time() - last_timer_action
            if elapsed_time_timer >= timer_interval:
                print("\n=== Melakukan tindakan timer (klik koordinat tambahan) ===\n")
                print("Mengklik koordinat (101, 60)")
                time.sleep(default_delay)
                pyautogui.click(101, 60)
                time.sleep(default_delay)
                print("Mengklik koordinat (1055, 64)")
                time.sleep(default_delay)
                pyautogui.click(1055, 64)
                time.sleep(default_delay)
                last_timer_action = time.time()

            print("Satu siklus urutan selesai (atau terhenti). Mengulang dari awal.")

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    print("Pastikan tab target aktif dan terlihat di layar.")
    print("Pastikan file 'angka_3.png' dan 'angka_6.png' berada di direktori yang sama dengan skrip ini.")
    print("Pastikan Tesseract OCR terinstal dan berada dalam PATH Anda agar pencarian teks berfungsi.")
    input("Tekan Enter untuk memulai...\nTekan Ctrl+C untuk menghentikan.")
    auto_klik_urutan_dengan_prioritas_3_6_timer_screenshot_fixed()
