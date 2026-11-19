"""Penyimpanan dan pembacaan data produk dari file CSV."""

import csv
import os

from product import Product

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "products.csv")
FIELDNAMES = ["product_id", "name", "category", "price", "stock"]


class StorageError(Exception):
    """Dilempar ketika file data rusak dan tidak bisa dibaca."""


class Storage:
    """Menyimpan dan memuat daftar produk dari/ke file CSV."""

    def __init__(self, filepath=DEFAULT_PATH):
        self.filepath = filepath
        self.warnings = []

    def save(self, products):
        """Menulis seluruh produk ke file CSV.

        Data ditulis ke file sementara lebih dulu, baru menggantikan file
        asli, sehingga file lama tidak rusak jika penulisan gagal.
        """
        folder = os.path.dirname(self.filepath)
        if folder:
            os.makedirs(folder, exist_ok=True)

        temp_path = self.filepath + ".tmp"
        try:
            with open(temp_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()
                for product in products:
                    writer.writerow({
                        "product_id": product.product_id,
                        "name": product.name,
                        "category": product.category,
                        "price": product.price,
                        "stock": product.stock,
                    })
            os.replace(temp_path, self.filepath)
        except OSError as error:
            raise StorageError(f"Gagal menyimpan data: {error}")

    def load(self):
        """Membaca produk dari file CSV.

        Raises:
            FileNotFoundError: file belum ada.
            StorageError: file rusak (header salah atau tidak bisa dibaca).

        Baris yang rusak dilewati dan dicatat di self.warnings.
        """
        self.warnings = []
        products = []

        try:
            with open(self.filepath, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                if reader.fieldnames is None or set(FIELDNAMES) - set(reader.fieldnames):
                    raise StorageError("Header file CSV tidak sesuai.")

                for line_number, row in enumerate(reader, start=2):
                    try:
                        products.append(Product(
                            row["product_id"],
                            row["name"],
                            row["category"],
                            row["price"],
                            row["stock"],
                        ))
                    except (ValueError, TypeError) as error:
                        self.warnings.append(f"Baris {line_number} dilewati: {error}")
        except (UnicodeDecodeError, csv.Error) as error:
            raise StorageError(f"File tidak dapat dibaca: {error}")

        return products
