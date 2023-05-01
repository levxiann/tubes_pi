from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    class LoginLevel(models.TextChoices):
        SUPERADMIN = "SA", "Super Admin"
        ADMIN = "A", "Admin"
        EMPLOYEE = "E", "Employee"
        CUSTOMER = "C", "Customer"

    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100, unique = True)
    username = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 100, null = True)
    phone_number = models.CharField(max_length = 20, unique = True)
    level = models.CharField(max_length = 2, choices = LoginLevel.choices, default = LoginLevel.CUSTOMER)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Shop(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 255)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class ShopPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length = 100)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.BigIntegerField()
    stock = models.IntegerField()
    status = models.BooleanField(default=False)
    description = models.CharField(max_length = 255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = "CA", "Cash"
        CREDIT = "CR", "Credit"
        DEBIT = "DE", "Debit"
        OVO = "O", "Ovo"
        GOPAY = "G", "Gopay"
        DANA = "D", "Dana"
    
    class PaymentStatus(models.TextChoices):
        PAID = "P", "Paid"
        NOTPAID = "NP", "Not Paid"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length = 2, choices = PaymentType.choices) 
    total_price = models.BigIntegerField()
    payment_date = models.DateTimeField(null = True)
    status = models.CharField(max_length = 2, choices = PaymentStatus.choices, default = PaymentStatus.NOTPAID) 
    created = models.DateTimeField(auto_now_add=True)

    products = models.ManyToManyField(Product, through="PaymentDetail")

    def __str__(self):
        return str(self.id)

class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
