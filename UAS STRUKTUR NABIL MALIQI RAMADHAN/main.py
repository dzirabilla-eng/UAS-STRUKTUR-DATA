import os

rundown_hashmap = {}
antrian_queue = [] # Isinya nanti kode tiket per orang (cth: VIP-12-1, VIP-12-2)

def load_dari_csv():
    if os.path.exists("lineup.csv"):
        file = open("lineup.csv", "r")
        file.readline() 
        for baris in file:
            data = baris.strip().split(",")
            if len(data) == 4:
                id_artis = data[0].strip()
                rundown_hashmap[id_artis] = {
                    "nama": data[1].strip(),
                    "jam": data[2].strip(),
                    "panggung": data[3].strip()
                }
        file.close()

def simpan_ke_csv():
    file = open("lineup.csv", "w")
    file.write("id,nama,jam,panggung\n")
    for id_artis, detail in rundown_hashmap.items():
        file.write(f"{id_artis},{detail['nama']},{detail['jam']},{detail['panggung']}\n")
    file.close()

def main():
    load_dari_csv() 
    
    while True:
        print("\n==============================================")
        print("    SYSTEM MANAGEMENT PANITIA KONSER (EO)")
        print("==============================================")
        print("1. Tambah Artis ke Rundown [Create]")
        print("2. Lihat & Urutkan Jadwal Tampil [Read & Sorting]")
        print("3. Edit Jadwal Artis [Update & Search]")
        print("4. Hapus Artis dari Rundown [Delete]")
        print("5. Sistem Scanner Gate Pintu Masuk [Queue]")
        print("6. Simpan Data & Keluar")
        
        pilih = input("Pilih menu (1-6): ").strip()

# --- MENU 1: CREATE ---
        if pilih == "1":
            print("\n--- TAMBAH ARTIS BARU ---")
            id_artis = input("Masukkan Nomor Urut (contoh: 001): ").strip()
            nama = input("Masukkan Nama Artis/Band: ").strip()
            jam = input("Masukkan Jam Tampil (contoh: 19:00): ").strip()
            panggung = input("Masukkan Nama Panggung: ").strip()
            
            rundown_hashmap[id_artis] = {"nama": nama, "jam": jam, "panggung": panggung}
            print("✅ Artis berhasil ditambahkan!")

# --- MENU 2: READ & SORTING ---
        elif pilih == "2":
            print("\n--- JADWAL RUNDOWN FESTIVAL ---")
            if not rundown_hashmap:
                print("⚠️ Jadwal rundown masih kosong!")
            else:
                daftar_artis = []
                for id_artis, detail in rundown_hashmap.items():
                    daftar_artis.append({
                        "id": id_artis,
                        "nama": detail["nama"],
                        "jam": detail["jam"],
                        "panggung": detail["panggung"]
                    })
                
                n = len(daftar_artis)
                for i in range(n):
                    for j in range(0, n-i-1):
                        if daftar_artis[j]["jam"] > daftar_artis[j+1]["jam"]:
                            daftar_artis[j], daftar_artis[j+1] = daftar_artis[j+1], daftar_artis[j]
                
                print(f"{'ID':<6} | {'NAMA ARTIS':<20} | {'JAM':<8} | {'PANGGUNG'}")
                print("-" * 60)
                for artis in daftar_artis:
                    print(f"{artis['id']:<6} | {artis['nama']:<20} | {artis['jam']:<8} | {artis['panggung']}")

# --- MENU 3: UPDATE & SEARCHING ---
        elif pilih == "3":
            print("\n--- EDIT JADWAL ARTIS ---")
            id_artis = input("Masukkan ID Artis yang mau diedit: ").strip()
            
            if id_artis in rundown_hashmap:
                nama_b = input("Masukkan Nama Baru: ").strip()
                jam_b = input("Masukkan Jam Baru: ").strip()
                pang_b = input("Masukkan Panggung Baru: ").strip()
                
                rundown_hashmap[id_artis] = {"nama": nama_b, "jam": jam_b, "panggung": pang_b}
                print("✅ Data jadwal berhasil diperbarui!")
            else:
                print("❌ ID artis tidak ditemukan!")

# --- MENU 4: DELETE ---
        elif pilih == "4":
            print("\n--- HAPUS ARTIS ---")
            id_artis = input("Masukkan ID Artis yang akan dihapus: ").strip()
            
            if id_artis in rundown_hashmap:
                del rundown_hashmap[id_artis]
                print("🗑️ Artis berhasil dihapus dari Rundown.")
            else:
                print("❌ ID artis tidak ditemukan!")

# --- MENU 5: QUEUE (VERSI KATEGORI TIKET) ---
        elif pilih == "5":
            print("\n--- SISTEM SCANNER GATE PINTU MASUK ---")
            print("a. Scan Tiket Masuk Masal (Enqueue)")
            print("b. Validasi Orang Terdepan untuk Buka Pintu (Dequeue)")
            sub_pilih = input("Pilih tindakan (a/b): ").strip().lower()
            
            if sub_pilih == "a":
                print("\n[ PILIH KATEGORI TIKET ]")
                print("1. VIP")
                print("2. FESTIVAL")
                print("3. REGULER")
                pilihan_kat = input("Pilih kategori (1-3): ").strip()
                
                if pilihan_kat == "1":
                    prefix = "VIP"
                elif pilihan_kat == "2":
                    prefix = "FST" # Festival
                elif pilihan_kat == "3":
                    prefix = "REG" # Reguler
                else:
                    print("❌ Pilihan kategori salah! Otomatis set ke REGULER.")
                    prefix = "REG"
                
                jumlah_input = input(f"Berapa jumlah tiket {prefix} yang dibawa?: ").strip()
                
                if jumlah_input.isdigit():
                    jumlah_tiket = int(jumlah_input)
                    for i in range(1, jumlah_tiket + 1):
                        nomor_unik = len(antrian_queue) + i
                        tiket_id = f"{prefix}-{nomor_unik}"
                        
                        antrian_queue.append(tiket_id)
                        print(f"  -> Tiket '{tiket_id}' masuk antrian gerbang.")
                    print(f"✅ Berhasil memasukkan {jumlah_tiket} tiket {prefix} ke barisan antrian!")
                else:
                    print("❌ Input salah! Jumlah tiket harus berupa angka.")
                
            elif sub_pilih == "b":
                if len(antrian_queue) > 0:
                    tiket_masuk = antrian_queue.pop(0) # Tetap FIFO (First In, First Out)
                    print(f"📢 VALID! Kategori {tiket_masuk.split('-')[0]} nomor {tiket_masuk.split('-')[1]} silakan masuk!")
                else:
                    print("⚠️ Tidak ada antrian di gerbang. Pintu ditutup.")
            else:
                print("❌ Pilihan tindakan tidak valid.")

# --- MENU 6: EXIT ---
        elif pilih == "6":
            simpan_ke_csv()
            print("💾 Semua data telah disimpan ke lineup.csv. Program selesai!")
            break
        else:
            print("❌ Pilihan menu tidak tersedia! Silakan ketik angka 1 sampai 6.")

if __name__ == "__main__":
    main()