import difflib

def is_match(user_ing, recipe_ing, threshold=0.7):
    """Cek apakah satu bahan user cocok dengan satu bahan resep."""
    user_ing = user_ing.lower().strip()
    recipe_ing = recipe_ing.lower().strip()

    # Cek exact match atau substring (Fitur F03: misal "bawang" cocok dengan "bawang merah")
    if user_ing in recipe_ing or recipe_ing in user_ing:
        return True

    # Cek fuzzy match menggunakan SequenceMatcher untuk mengatasi typo ringan
    ratio = difflib.SequenceMatcher(None, user_ing, recipe_ing).ratio()
    return ratio >= threshold

def hitung_skor(list_bahan_user, list_bahan_resep):
    """
    Menghitung persentase kelengkapan bahan.
    Mengembalikan persentase, list bahan yang tersedia, dan list bahan yang kurang.
    """
    if not list_bahan_resep:
        return 0.0, [], []

    bahan_terpenuhi = 0
    bahan_ada = []
    bahan_kurang = []

    for req_ing in list_bahan_resep:
        nama_req = req_ing['name']
        matched = False
        
        for usr_ing in list_bahan_user:
            if is_match(usr_ing, nama_req):
                matched = True
                break

        if matched:
            bahan_terpenuhi += 1
            bahan_ada.append(nama_req)
        else:
            bahan_kurang.append(nama_req)

    # Menghitung persentase (Fitur F04)
    persentase = (bahan_terpenuhi / len(list_bahan_resep)) * 100
    return round(persentase), bahan_ada, bahan_kurang