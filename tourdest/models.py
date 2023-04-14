from django.db import models

# Create your models here.
class User(models.Model):
    class LoginLevel(models.TextChoices):
        SUPERADMIN = "SA", _("Super Admin")
        ADMIN = "A", _("Admin")
        EMPLOYEE = "E", _("Employee")
        CUSTOMER = "C", _("Customer")

    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100, unique = True)
    username = models.CharField(max_length = 50, unique = True)
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
    employees = models.ManyToManyField(User, through="ShopPosition")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

class ShopPosition(models.Model):
    user = models.ForeignKey(User, on_update=models.CASCADE)
    shop = models.ForeignKey(Shop, on_update=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length = 100)
    shop = models.ForeignKey(Shop, on_update=models.CASCADE)
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
        CASH = "CA", _("Cash")
        CREDIT = "CR", _("Credit")
        DEBIT = "DE", _("Debit")
        OVO = "O", _("Ovo")
        GOPAY = "G", _("Gopay")
        DANA = "D", _("Dana")
    
    class PaymentStatus(models.TextChoices):
        PAID = "P", _("Paid")
        NOTPAID = "NP", _("Not Paid")

    user = models.ForeignKey(User, on_update=models.CASCADE)
    shop = models.ForeignKey(Shop, on_update=models.CASCADE)
    payment_type = models.CharField(max_length = 2, choices = PaymentType.choices) 
    total_price = models.BigIntegerField()
    payment_date = models.DateTimeField(null = True)
    status = models.CharField(max_length = 2, choices = PaymentStatus.choices, default = PaymentStatus.NOTPAID) 
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class PaymentDetail(models.Model):
    payment = models.ForeignKey(Payment, on_update=models.CASCADE)
    product = models.ForeignKey(Product, on_update=models.CASCADE)
    quantity = models.IntegerField()
    price = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
