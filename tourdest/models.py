from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # 4 Pilihan Level User
    class LoginLevel(models.TextChoices):
        SUPERADMIN = "SA", "Super Admin"
        ADMIN = "A", "Admin"
        EMPLOYEE = "E", "Employee"
        CUSTOMER = "C", "Customer"

    # Nama
    name = models.CharField(max_length = 100)
    # Email unik setiap user
    email = models.EmailField(max_length = 100, unique = True)
    # Username unik setiap user
    username = models.CharField(max_length = 50, unique = True)
    # Password (akan dihash ketika disimpan ke database)
    password = models.CharField(max_length = 100, null = True)
    # No. Telp. unik setiap user
    phone_number = models.CharField(max_length = 20, unique = True)
    # Level User (4 pilihan)
    level = models.CharField(max_length = 2, choices = LoginLevel.choices, default = LoginLevel.CUSTOMER)
    # Status User (true = bekerja di sebuah toko, false = tidak bekerja)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # mengembalikan nama user ketika object dibuat
    def __str__(self):
        return self.name

    # Urut berdasarkan nama
    class Meta:
        ordering = ('name',)

class Shop(models.Model):
    # Nama toko
    name = models.CharField(max_length = 100)
    # Lokasi toko
    location = models.CharField(max_length = 255)
    # Status toko (true = aktif, false = tidak aktif)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # mengembalikan nama toko ketika object dibuat
    def __str__(self):
        return self.name

    # Urut berdasarkan nama
    class Meta:
        ordering = ('name',)

class ShopPosition(models.Model):
    # Foreign Key User yang terhubung ke Toko
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign Key Toko yang terhubung ke User
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    # Nama Produk
    name = models.CharField(max_length = 100)
    # Foreign Key Toko yang menujual Produk
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # Harga produk
    price = models.BigIntegerField()
    # Stok produk
    stock = models.IntegerField()
    # Status produk (true = aktif, false = tidak aktif)
    status = models.BooleanField(default=False)
    # Keterangan produk
    description = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True)

    # Mengembalikan nama produk ketika object dibuat
    def __str__(self):
        return self.name

    # Diurutkan berdasarkan nama produk
    class Meta:
        ordering = ('name',)

class Payment(models.Model):
    # 3 Pilihan Status Pembayaran 
    class PaymentStatus(models.TextChoices):
        PAID = "P", "Paid"
        NOTPAID = "NP", "Not Paid"
        REJECTED = "R", "Rejected"
    
    # Diurutkan berdasarkan primary key
    class Meta:
        ordering = ('-pk',)

    # Foreign Key User yang melakukan transaksi
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign Key toko tempat dilakukan transaksi
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # Foreign Key produk yang dibeli
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Jumlah Produk yang dibeli
    quantity = models.IntegerField()
    # Jumlah Produk yang ditolak (quantity akan dipindahkan ke kolom ini apabila status REJECTED)
    quantity_reject = models.IntegerField(default = 0)
    # Total harga produk yang dibeli
    total_price = models.BigIntegerField()
    # Tanggal pembayaran
    payment_date = models.DateTimeField(null = True)
    # Status transaksi (3 pilihan)
    status = models.CharField(max_length = 2, choices = PaymentStatus.choices, default = PaymentStatus.NOTPAID) 
    created = models.DateTimeField(auto_now_add=True)

    # Mengembalikan id traksaksi ketika object dibuat
    def __str__(self):
        return str(self.id)
