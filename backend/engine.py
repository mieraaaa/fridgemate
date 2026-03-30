import json
import os
from backend.matcher import hitung_skor

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'resep.json')

def load_database():
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File database tidak ditemukan di {DB_PATH}")
        return []

def cari_resep(list_bahan_user, filter_waktu_cepat=False):
    """Fungsi utama untuk mencari dan mengurutkan resep."""
    database_resep = load_database()['resep']
    hasil = []

    for resep in database_resep:
        # Fitur F08 (Opsional): Filter waktu masak di bawah 20 menit
        if filter_waktu_cepat and resep.get('time_minutes', 999) >= 20:
            continue

        skor, bahan_ada, bahan_kurang = hitung_skor(list_bahan_user, resep['ingredients'])

        # Hanya masukkan ke hasil jika ada minimal 1 bahan yang cocok
        if skor > 0:
            resep_cocok = resep.copy()
            resep_cocok['match_percentage'] = skor
            resep_cocok['available_ingredients'] = bahan_ada
            resep_cocok['missing_ingredients'] = bahan_kurang
            hasil.append(resep_cocok)

        # Fitur F04: Resep diurutkan dari persentase tertinggi (Descending)
        hasil.sort(key=lambda x: x['match_percentage'], reverse=True)

    return hasil

# --- Variabel Global untuk Cache ---
# Kita simpan daftar bahan di memori agar sistem tidak perlu
# membaca file JSON berulang kali setiap pengguna mengetik 1 huruf.
_CACHE_BAHAN_UNIK = []

def get_semua_bahan_unik():
    """Mengumpulkan semua nama bahan unik dari database."""
    global _CACHE_BAHAN_UNIK
    
    # Jika cache masih kosong, baca dari database
    if not _CACHE_BAHAN_UNIK:
        database_resep = load_database()['resep']
        semua_bahan = set() # Menggunakan set untuk otomatis membuang duplikat
        
        for resep in database_resep:
            for bahan in resep.get('ingredients', []):
                # Ambil nama bahan, ubah ke lowercase
                semua_bahan.add(bahan['name'].lower().strip())
                
        # Simpan ke cache dalam bentuk list yang sudah diurutkan abjad
        _CACHE_BAHAN_UNIK = sorted(list(semua_bahan))
        
    return _CACHE_BAHAN_UNIK

def dapatkan_saran_bahan(keyword, max_hasil=5):
    """
    Mengembalikan daftar saran bahan berdasarkan input pengguna.
    """
    if not keyword:
        return []

    keyword = keyword.lower().strip()
    semua_bahan = get_semua_bahan_unik()

    # Cari bahan yang mengandung keyword yang diketik
    hasil = [bahan for bahan in semua_bahan if keyword in bahan]

    # Urutkan: bahan yang diawali dengan keyword ditaruh di paling atas
    # Contoh: ketik "ga", "garlic" muncul lebih dulu daripada "sugar"
    hasil.sort(key=lambda x: (not x.startswith(keyword), x))

    # Batasi jumlah saran yang muncul agar UI tidak kepenuhan
    return hasil[:max_hasil]

# ==========================================
# BLOK TESTING LOKAL
# ==========================================
if __name__ == '__main__':
    # 1. Test Fitur Autocomplete / Suggestion (F01)
    print("--- TESTING AUTOCOMPLETE ---")
    kata_kunci = "ch"
    print(f"User mengetik: '{kata_kunci}'")
    saran = dapatkan_saran_bahan(kata_kunci)
    print(f"Saran yang muncul: {saran}\n")
    
    kata_kunci_2 = "to"
    print(f"User mengetik: '{kata_kunci_2}'")
    saran_2 = dapatkan_saran_bahan(kata_kunci_2)
    print(f"Saran yang muncul: {saran_2}\n")

    # 2. Test Fitur Pencarian Resep Utama (F02, F03, F04)
    print("--- TESTING PENCARIAN RESEP ---")
    input_dummy = ['spinach', 'eggs', 'cheese']
    print(f"Mencari resep dengan bahan: {input_dummy}...")

    hasil_pencarian = cari_resep(input_dummy)

    if not hasil_pencarian:
        print("Tidak ada resep yang cocok.")
    else:
        print(f"Ditemukan {len(hasil_pencarian)} resep:\n")
        # Menampilkan 3 hasil teratas saja untuk testing
        for r in hasil_pencarian[:3]:
            print(f"- {r['title']} ({r['match_percentage']}% Match)")