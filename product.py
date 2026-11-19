"""Model data untuk satu produk Buzinice."""


class Product:
    """Mewakili satu produk yang dijual oleh sebuah usaha."""

    EDITABLE_FIELDS = ("name", "category", "price", "stock")

    def __init__(self, product_id, name, category, price, stock):
        self.product_id = str(product_id).strip()
        self.name = str(name).strip()
        self.category = str(category).strip()
        self.price = self.to_price(price)
        self.stock = self.to_stock(stock)
        self.validate()

    @staticmethod
    def to_price(value):
        """Mengubah harga ke float dan memastikan nilainya valid."""
        try:
            price = float(value)
        except (TypeError, ValueError):
            raise ValueError("Harga harus berupa angka.")
        if price < 0:
            raise ValueError("Harga tidak boleh negatif.")
        return price

    @staticmethod
    def to_stock(value):
        """Mengubah stok ke int dan memastikan nilainya valid."""
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError("Stok harus berupa angka bulat.")
        if number != int(number):
            raise ValueError("Stok harus berupa angka bulat.")
        if number < 0:
            raise ValueError("Stok tidak boleh negatif.")
        return int(number)

    def validate(self):
        """Memastikan seluruh data produk masuk akal."""
        if not self.product_id:
            raise ValueError("ID produk tidak boleh kosong.")
        if not self.name:
            raise ValueError("Nama produk tidak boleh kosong.")
        if not self.category:
            raise ValueError("Kategori produk tidak boleh kosong.")

    def update(self, **kwargs):
        """Mengubah atribut produk menggunakan **kwargs.

        Contoh: product.update(price=7000, stock=15)
        Perubahan hanya diterapkan jika seluruh nilai valid.
        """
        new_values = {}
        for field, value in kwargs.items():
            if field not in self.EDITABLE_FIELDS:
                raise ValueError(f"Atribut '{field}' tidak dapat diubah.")
            if field == "price":
                value = self.to_price(value)
            elif field == "stock":
                value = self.to_stock(value)
            else:
                value = str(value).strip()
                if not value:
                    raise ValueError(f"{field} tidak boleh kosong.")
            new_values[field] = value

        for field, value in new_values.items():
            setattr(self, field, value)

    def __str__(self):
        return (
            f"{self.product_id:<6} | {self.name:<15} | "
            f"{self.category:<12} | Rp{self.price:>10,.0f} | {self.stock:>4}"
        )
