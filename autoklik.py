import pyautogui
import time
import math
import re
import pytesseract

# Konfigurasikan path Tesseract (sesuaikan dengan sistem Anda)
try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Contoh Windows
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
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

def auto_klik_urutan_dengan_delay_spesifik_berulang_dengan_timer_tambahan_screenshot():
    """
    Melakukan auto klik pada urutan angka, dengan penanganan kegagalan khusus untuk angka 3 dan 6,
    serta mengklik koordinat tambahan setiap 10 menit.
    Mulai dari nomor 1.
    """
    try:
        koordinat_angka_statis = {
            1: (918, 804),
            2: (911, 1073),
            4: (1759, 809),
            5: (1748, 1073),
        }

        urutan_klik_awal = [2, 3, 6, 4, 5] # Urutan setelah klik pertama (angka 1)
        urutan_klik = list(urutan_klik_awal)
        delay_sebelum = {1: 0.5, 2: 0.5, 4: 0.5, 5: 0.5}
        delay_sesudah = {1: 0.5, 2: 0.5, 3: 0.5, 4: 0.5, 5: 0.5, 6: 0.5}
        default_delay = 1.5
        timer_interval = 600
        last_timer_action = time.time()
        gagal_3_dalam_urutan = False
        gagal_6_dalam_urutan = False
        siklus_berhasil = False

        # Koordinat untuk klik jika angka 3 atau 6 tidak muncul setelah timeout
        koordinat_klik_jika_3_tidak_muncul = (96, 65)
        koordinat_klik_jika_6_tidak_muncul = (1055, 63)
        timeout_3 = 120  # 2 menit dalam detik
        timeout_6 = 120  # 2 menit dalam detik
        waktu_mulai_pencarian_3 = 0
        waktu_mulai_pencarian_6 = 0
        waktu_penundaan_3_berakhir = 0
        waktu_penundaan_6_berakhir = 0
        penundaan_3_sedang_berlangsung = False
        penundaan_6_sedang_berlangsung = False
        durasi_penundaan = 20

        print(f"Memulai auto klik. Angka 1 pertama, lalu urutan. Pencarian proaktif untuk 3 & 6 dengan timeout {timeout_3} detik. Timer setiap {timer_interval // 60} menit.")

        # Klik angka 1 pertama kali
        print("\n=== Klik pertama: Angka 1 ===")
        if 1 in koordinat_angka_statis:
            print(f"Menunggu {delay_sebelum.get(1, default_delay)} detik sebelum klik angka 1...")
            time.sleep(delay_sebelum.get(1, default_delay))
            x1, y1 = koordinat_angka_statis[1]
            print(f"Mengklik angka 1 di ({x1}, {y1})")
            time.sleep(default_delay)
            pyautogui.click(x1, y1)
            print(f"Menunggu {delay_sesudah.get(1, default_delay)} detik setelah klik angka 1...")
            time.sleep(delay_sesudah.get(1, default_delay))
        else:
            print("Koordinat untuk angka 1 tidak ditemukan.")

        while True:
            gagal_3_dalam_urutan = False
            gagal_6_dalam_urutan = False
            angka_3_sudah_dicari = False
            angka_6_sudah_dicari = False

            for index, angka in enumerate(urutan_klik): # Loop melalui urutan angka yang akan diklik
                berhasil_klik = False

                # Cek apakah sedang dalam masa penundaan untuk angka 1, 2, dan 3
                if (angka in [1, 2, 3]) and penundaan_3_sedang_berlangsung:
                    if time.time() < waktu_penundaan_3_berakhir:
                        print(f"Melewati angka {angka} karena penundaan 20 detik sedang berlangsung.")
                        continue  # Lewati iterasi ini, jangan klik
                    else:
                        penundaan_3_sedang_berlangsung = False  # Penundaan selesai, reset flag
                        print(f"Penundaan 20 detik untuk angka 1, 2, dan 3 selesai.")

                # Cek apakah sedang dalam masa penundaan untuk angka 4
                if (angka in [4]) and penundaan_6_sedang_berlangsung:
                    if time.time() < waktu_penundaan_6_berakhir:
                        print(f"Melewati angka {angka} karena penundaan 20 detik sedang berlangsung.")
                        continue  # Lewati iterasi ini, jangan klik
                    else:
                        penundaan_6_sedang_berlangsung = False  # Penundaan selesai, reset flag
                        print(f"Penundaan 20 detik untuk angka 4 selesai.")

                if angka in koordinat_angka_statis:
                    delay_pre = delay_sebelum.get(angka, default_delay)
                    print(f"Menunggu {delay_pre} detik sebelum klik angka {angka}...")
                    time.sleep(delay_pre)
                    x, y = koordinat_angka_statis[angka]
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
                        waktu_mulai_pencarian_3 = 0  # Reset timer
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
                        siklus_berhasil = True
                        waktu_mulai_pencarian_6 = 0  # Reset timer
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
                        waktu_mulai_pencarian_3 = 0  # Reset timer setelah klik
                        gagal_3_dalam_urutan = True  # Set flag gagal
                        penundaan_3_sedang_berlangsung = True
                        waktu_penundaan_3_berakhir = time.time() + durasi_penundaan
                        print(f"Menunda klik angka 1, 2, dan 3 selama {durasi_penundaan} detik.")
                        continue  # Lanjutkan ke iterasi berikutnya dari loop while

                if not berhasil_klik and angka == 6:
                    if time.time() - waktu_mulai_pencarian_6 >= timeout_6:
                        print(f"Angka 6 tidak ditemukan setelah {timeout_6} detik. Mengklik koordinat {koordinat_klik_jika_6_tidak_muncul}")
                        pyautogui.click(koordinat_klik_jika_6_tidak_muncul)
                        time.sleep(default_delay)
                        waktu_mulai_pencarian_6 = 0  # Reset timer setelah klik
                        gagal_6_dalam_urutan = True  # Set flag gagal
                        penundaan_6_sedang_berlangsung = True
                        waktu_penundaan_6_berakhir = time.time() + durasi_penundaan
                        print(f"Menunda klik angka 4 selama {durasi_penundaan} detik.")
                        continue  # Lanjutkan ke iterasi berikutnya dari loop while

            # Bagian ini berada di luar loop for, jadi tidak ada masalah dengan 'break'
            if gagal_3_dalam_urutan and gagal_6_dalam_urutan:
                print("Gambar angka 3 dan 6 tidak ditemukan dalam urutan. Memulai ulang dari angka 1.")
                urutan_klik = list(urutan_klik_awal)
                continue # Kembali ke awal loop while

            elif siklus_berhasil:
                print("\n=== Siklus berhasil mencapai angka 6. Kembali ke koordinat (918, 804). ===")
                pyautogui.click(918, 804)
                time.sleep(default_delay)
                print("Mengklik koordinat (918, 804).")
                urutan_klik = list(urutan_klik_awal)
                siklus_berhasil = False
                continue # Kembali ke awal loop while

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

            print("Satu siklus selesai. Mengulang...")
            # Tidak ada 'break' di sini.  Loop while akan terus berlanjut.

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    print("Pastikan tab target aktif dan terlihat di layar.")
    print("Pastikan file 'angka_3.png' dan 'angka_6.png' berada di direktori yang sama dengan skrip ini.")
    print("Pastikan Tesseract OCR terinstal dan berada dalam PATH Anda agar pencarian teks berfungsi.")
    input("Tekan Enter untuk memulai...\nTekan Ctrl+C untuk menghentikan.")
    auto_klik_urutan_dengan_delay_spesifik_berulang_dengan_timer_tambahan_screenshot()
