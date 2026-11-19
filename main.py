"""Program utama Buzinice - Progress 3 (Search, Sorting & File Handling)."""

from product import Product
from inventory import Inventory


def print_header():
    print("=" * 62)
    print("  BUZINICE | Product & Inventory Management")
    print("=" * 62)


def print_menu():
    print("\nMENU")
    print("1. Tampilkan produk")
    print("2. Tambah produk")
    print("3. Ubah produk")
    print("4. Hapus produk")
    print("5. Cari produk")
    print("6. Urutkan produk")
    print("0. Keluar")


def show_products(inventory, products=None):
    """Menampilkan produk dalam bentuk tabel (default: semua produk)."""
    if products is None:
        products = inventory.get_all_products()
    if not products:
        print("\nBelum ada produk.")
        return

    print("\n" + "-" * 62)
    print(f"{'ID':<6} | {'Nama':<15} | {'Kategori':<12} | {'Harga':>12} | {'Stok':>4}")
    print("-" * 62)
    for product in products:
        print(product)
    print("-" * 62)
    print(
        f"Ditampilkan: {len(products)} | "
        f"Total produk: {inventory.total_products()} | "
        f"Total stok: {inventory.total_stock()}"
    )


def add_product(inventory):
    """Meminta input pengguna lalu menambahkan produk baru."""
    print("\n--- Tambah Produk ---")
    product_id = input("ID produk  : ")
    name = input("Nama produk: ")
    category = input("Kategori   : ")
    price = input("Harga      : ")
    stock = input("Stok       : ")

    try:
        inventory.add_product(Product(product_id, name, category, price, stock))
        print("Produk berhasil ditambahkan.")
    except ValueError as error:
        print(f"Input tidak valid: {error}")


def edit_product(inventory):
    """Mengubah data produk; kolom yang dikosongkan tidak diubah."""
    print("\n--- Ubah Produk ---")
    product_id = input("ID produk yang diubah: ")
    product = inventory.find_by_id(product_id)
    if product is None:
        print("Produk tidak ditemukan.")
        return

    print(f"Data saat ini : {product}")
    print("(Kosongkan input jika tidak ingin mengubah)")
    fields = {
        "name": input("Nama baru     : "),
        "category": input("Kategori baru : "),
        "price": input("Harga baru    : "),
        "stock": input("Stok baru     : "),
    }
    # Hanya kolom yang diisi yang dikirim sebagai **kwargs.
    changes = {key: value for key, value in fields.items() if value.strip()}

    try:
        updated = inventory.update_product(product_id, **changes)
        print(f"Produk berhasil diubah: {updated}")
    except ValueError as error:
        print(f"Gagal mengubah: {error}")


def delete_product(inventory):
    """Menghapus produk setelah konfirmasi."""
    print("\n--- Hapus Produk ---")
    product_id = input("ID produk yang dihapus: ")
    product = inventory.find_by_id(product_id)
    if product is None:
        print("Produk tidak ditemukan.")
        return

    confirm = input(f"Yakin hapus '{product.name}'? (y/n): ").strip().lower()
    if confirm == "y":
        inventory.remove_product(product_id)
        print("Produk berhasil dihapus.")
    else:
        print("Penghapusan dibatalkan.")


def search_product(inventory):
    """Mencari produk berdasarkan kata kunci."""
    print("\n--- Cari Produk ---")
    keyword = input("Kata kunci (ID/nama/kategori): ")
    results = inventory.search_products(keyword)
    if not results:
        print("Produk tidak ditemukan.")
        return
    show_products(inventory, results)


def sort_product(inventory):
    """Mengurutkan produk berdasarkan nama, harga, atau stok."""
    print("\n--- Urutkan Produk ---")
    print("1. Nama   2. Harga   3. Stok")
    keys = {"1": "name", "2": "price", "3": "stock"}
    key = keys.get(input("Urutkan berdasarkan: ").strip())
    if key is None:
        print("Pilihan tidak tersedia.")
        return

    order = input("Urutan (1 = naik, 2 = turun): ").strip()
    if order not in ("1", "2"):
        print("Pilihan tidak tersedia.")
        return

    show_products(inventory, inventory.sort_products(key, descending=(order == "2")))


def print_messages(inventory):
    """Menampilkan pesan peringatan dari proses file."""
    for message in inventory.pop_messages():
        print(f"[!] {message}")


def main():
    inventory = Inventory()
    print_header()
    print_messages(inventory)

    actions = {
        "1": show_products,
        "2": add_product,
        "3": edit_product,
        "4": delete_product,
        "5": search_product,
        "6": sort_product,
    }

    while True:
        print_menu()
        choice = input("Pilih menu: ").strip()

        if choice == "0":
            print("Terima kasih telah menggunakan Buzinice.")
            break
        action = actions.get(choice)
        if action:
            action(inventory)
            print_messages(inventory)
        else:
            print("Pilihan tidak tersedia, coba lagi.")


if __name__ == "__main__":
    main()
