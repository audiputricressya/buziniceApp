"""Pengelolaan data inventaris Buzinice."""

import os

from product import Product
from storage import Storage, StorageError


class Inventory:
    """Menyimpan dan mengelola kumpulan objek Product (CRUD, cari, urut)."""

    # Kunci pengurutan: setiap kunci dipetakan ke fungsi lambda.
    SORT_KEYS = {
        "name": lambda product: product.name.lower(),
        "price": lambda product: product.price,
        "stock": lambda product: product.stock,
    }

    def __init__(self, storage=None):
        self.storage = storage or Storage()
        self.products = []
        self.messages = []
        self.load_data()

    # ---------- File handling ----------
    def load_data(self):
        """Memuat data dari file; memakai data awal jika file hilang/rusak."""
        try:
            loaded = self.storage.load()
        except FileNotFoundError:
            self.messages.append("File data belum ada, dibuat dengan data awal.")
            self.load_sample_data()
            return
        except StorageError as error:
            self.messages.append(f"File data rusak ({error}).")
            self.backup_corrupt_file()
            self.load_sample_data()
            return

        self.messages.extend(self.storage.warnings)
        for product in loaded:
            try:
                self._insert(product)
            except ValueError as error:
                self.messages.append(f"Produk dilewati: {error}")

    def backup_corrupt_file(self):
        """Mengganti nama file rusak menjadi .bak agar tidak tertimpa."""
        backup_path = self.storage.filepath + ".bak"
        try:
            os.replace(self.storage.filepath, backup_path)
            self.messages.append(f"File rusak disimpan sebagai {backup_path}.")
        except OSError:
            self.messages.append("File rusak tidak dapat dicadangkan.")

    def save(self):
        """Menyimpan data ke file; mengembalikan True jika berhasil."""
        try:
            self.storage.save(self.products)
            return True
        except StorageError as error:
            self.messages.append(str(error))
            return False

    def load_sample_data(self):
        """Mengisi data produk awal lalu menyimpannya ke file."""
        for product in (
            Product("P001", "Buku Tulis", "Alat Tulis", 5000, 10),
            Product("P002", "Pulpen", "Alat Tulis", 3000, 20),
            Product("P003", "Botol Minum", "Aksesori", 15000, 5),
        ):
            self._insert(product)
        self.save()

    def pop_messages(self):
        """Mengambil lalu mengosongkan pesan peringatan."""
        messages, self.messages = self.messages, []
        return messages

    # ---------- Pencarian ID ----------
    def find_by_id(self, product_id):
        """Mencari produk berdasarkan ID; None jika tidak ada."""
        for product in self.products:
            if product.product_id.lower() == str(product_id).strip().lower():
                return product
        return None

    # ---------- Create ----------
    def _insert(self, product):
        """Memasukkan produk ke daftar tanpa menyimpan ke file."""
        if not isinstance(product, Product):
            raise TypeError("Data yang ditambahkan harus berupa Product.")
        if self.find_by_id(product.product_id):
            raise ValueError(f"ID produk '{product.product_id}' sudah digunakan.")
        self.products.append(product)

    def add_product(self, product):
        """Menambahkan satu produk, mencegah ID duplikat, lalu menyimpan."""
        self._insert(product)
        self.save()

    def add_products(self, *args):
        """Menambahkan banyak produk sekaligus menggunakan *args."""
        for product in args:
            self._insert(product)
        self.save()

    # ---------- Read ----------
    def get_all_products(self):
        """Mengembalikan seluruh produk."""
        return self.products

    # ---------- Update ----------
    def update_product(self, product_id, **kwargs):
        """Mengubah informasi produk menggunakan **kwargs."""
        product = self.find_by_id(product_id)
        if product is None:
            raise ValueError("Produk tidak ditemukan.")
        if not kwargs:
            raise ValueError("Tidak ada data yang diubah.")
        product.update(**kwargs)
        self.save()
        return product

    # ---------- Delete ----------
    def remove_product(self, product_id):
        """Menghapus produk berdasarkan ID."""
        product = self.find_by_id(product_id)
        if product is None:
            raise ValueError("Produk tidak ditemukan.")
        self.products.remove(product)
        self.save()
        return product

    # ---------- Search & Sort ----------
    def search_products(self, keyword):
        """Mencari produk yang ID, nama, atau kategorinya memuat keyword."""
        keyword = str(keyword).strip().lower()
        if not keyword:
            return []
        return list(filter(
            lambda p: keyword in p.product_id.lower()
            or keyword in p.name.lower()
            or keyword in p.category.lower(),
            self.products,
        ))

    def sort_products(self, key, descending=False):
        """Mengembalikan daftar produk terurut berdasarkan name/price/stock."""
        if key not in self.SORT_KEYS:
            raise ValueError("Kunci pengurutan harus name, price, atau stock.")
        return sorted(self.products, key=self.SORT_KEYS[key], reverse=descending)

    # ---------- Ringkasan ----------
    def total_products(self):
        return len(self.products)

    def total_stock(self):
        return sum(product.stock for product in self.products)
