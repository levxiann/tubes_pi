from rest_framework import serializers
from tourdest.models import User
from tourdest.models import Shop
from tourdest.models import ShopPosition
from tourdest.models import Product
from tourdest.models import Payment
from tourdest.models import PaymentDetail
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100, allow_null=True)
    phone_number = serializers.CharField(max_length=20)
    level = serializers.ChoiceField(choices = [("SA", "Super Admin"), ("A", "Admin"), ("E", "Employee"), ("C", "Customer"),])
    status = serializers.BooleanField(default = False)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            validated_data['password'] = make_password(password)
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password', None)
        if password is not None:
            instance.password = make_password(password)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.level = validated_data.get('level', instance.level)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100, write_only=True)

class ShopSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=255)
    status = serializers.BooleanField(default = False)

    def create(self, validated_data):
        return Shop.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class ShopPositionSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only = True)
    shop = ShopSerializer(read_only = True)

    def create(self, validated_data):
        user_id = self.initial_data.get("user")
        validated_data["user_id"] = user_id
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        return ShopPosition.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_id = self.initial_data.get("user")
        shop_id = self.initial_data.get("shop")
        if user_id:
            instance.user_id = user_id
        if shop_id:
            instance.shop_id = shop_id
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    shop = ShopSerializer(read_only = True)
    price = serializers.IntegerField()
    stock = serializers.IntegerField()
    status = serializers.BooleanField(default = False)
    description = serializers.CharField(max_length=255)

    def create(self, validated_data):
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        shop_id = self.initial_data.get("shop")
        instance.name = validated_data.get('name', instance.name)
        if shop_id:
            instance.shop_id = shop_id
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class PaymentSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)
    shop = ShopSerializer(read_only=True)
    payment_type = serializers.ChoiceField(choices = [("CA", "Cash"), ("CR", "Credit"), ("DE", "Debit"), ("O", "Ovo"), ("G", "Gopay"), ("D", "Dana"),])
    total_price = serializers.IntegerField()
    payment_date = serializers.DateTimeField()
    status = serializers.ChoiceField(choices = [("P", "Paid"), ("NP", "Not Paid")])

    def create(self, validated_data):
        user_id = self.initial_data.get("user")
        validated_data["user_id"] = user_id
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_id = self.initial_data.get("user")
        shop_id = self.initial_data.get("shop")
        if user_id:
            instance.user_id = user_id
        if shop_id:
            instance.shop_id = shop_id
        instance.payment_type = validated_data.get('payment_type', instance.payment_type)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class PaymentDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    payment = PaymentSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        payment_id = self.initial_data.get("payment")
        validated_data["payment_id"] = payment_id
        product_id = self.initial_data.get("product")
        validated_data["product_id"] = product_id
        return PaymentDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        payment_id = self.initial_data.get("payment")
        product_id = self.initial_data.get("product")
        if payment_id:
            instance.payment_id = payment_id
        if product_id:
            instance.product_id = product_id
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def save(self):
        if self.instance:
            previous_quantity = self.instance.quantity
            instance = super().save()
            product = instance.product
            quantity_difference = instance.quantity - previous_quantity
            product.stock -= quantity_difference
        else:
            instance = super().save()
            product = instance.product
            product.stock -= instance.quantity
        product.save()
        return instance