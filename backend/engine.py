import json
import os
from backend.matcher import hitung_skor

# Path ke resep.json disesuaikan dengan struktur folder
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'resep.json')

def load_database():
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Handle if the root is a dictionary with a "resep" key
            if isinstance(data, dict) and 'resep' in data:
                return data['resep']
            return data
    except FileNotFoundError:
        print(f"Error: File database tidak ditemukan di {DB_PATH}")
        return []

def cari_resep(list_bahan_user):
    """Fungsi utama untuk mencari dan mengurutkan resep."""
    database_resep = load_database()
    hasil = []

    for resep in database_resep:

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

# ==========================================
# BLOK TESTING LOKAL
# ==========================================
if __name__ == '__main__':
    # Simulasi bahan yang diinput user
    input_dummy = ['spinach', 'eggs', 'cheese']
    print(f"Mencari resep dengan bahan: {input_dummy}...\n")

    hasil_pencarian = cari_resep(input_dummy)

    if not hasil_pencarian:
        print("Tidak ada resep yang cocok.")
    else:
        print(f"Ditemukan {len(hasil_pencarian)} resep:\n")
        for r in hasil_pencarian:
            print(f"- {r['title']} ({r['match_percentage']}% Match)")
            print(f"  Waktu Masak: {r.get('time_minutes')} menit")
            print(f"  Bahan tersedia : {r['available_ingredients']}")
            print(f"  Bahan kurang   : {r['missing_ingredients']}\n")