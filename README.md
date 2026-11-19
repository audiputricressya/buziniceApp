# Buzinice – Progress 3 (Search, Sorting & File Handling)

Buzinice adalah program manajemen produk dan inventaris sederhana untuk
membantu UMKM mencatat barang dagangan dan stoknya.

## Fitur
**Progress 1**
- Data produk awal dan menu interaktif di terminal.
- Menampilkan daftar produk beserta total produk dan total stok.

**Progress 2**
- CRUD produk: tambah, tampilkan, ubah, dan hapus.
- Validasi harga dan stok, serta pencegahan ID duplikat.
- Penggunaan `*args` (`add_products`) dan `**kwargs` (`update_product`).

**Progress 3**
- Pencarian produk berdasarkan kata kunci (ID, nama, atau kategori).
- Pengurutan berdasarkan nama, harga, dan stok (naik/turun) memakai `lambda`.
- Data disimpan ke `data/products.csv` memakai `with open()` dan otomatis
  dibaca saat program dibuka, sehingga data tidak hilang saat program ditutup.
- Penanganan file hilang atau rusak dengan `try-except`:
  - File belum ada -> dibuat otomatis dengan data awal.
  - File rusak (header salah / tidak terbaca) -> dicadangkan sebagai `.bak`
    lalu program memakai data awal.
  - Baris data rusak atau ID ganda -> dilewati dan ditampilkan sebagai peringatan.

## Struktur Proyek
```text
Buzinice/
├── main.py          # menjalankan program dan menu
├── product.py       # class Product + validasi
├── inventory.py     # class Inventory (CRUD, cari, urut)
├── storage.py       # class Storage (baca/tulis CSV)
├── data/
│   └── products.csv # data produk
├── README.md
└── .gitignore
```

## Cara Menjalankan
1. Pastikan Python 3 sudah terpasang.
2. Buka terminal di folder proyek.
3. Jalankan: `python main.py`

## Contoh Kode
```python
inventory.add_products(produk_a, produk_b)              # *args
inventory.update_product("P001", price=7000, stock=15)  # **kwargs
inventory.search_products("alat")                       # pencarian
inventory.sort_products("price", descending=True)       # pengurutan (lambda)
```

## Rencana Berikutnya
- Laporan dan statistik inventaris.
- Pengujian otomatis.
