from rest_framework import serializers
from tourdest.models import User
from tourdest.models import Shop
from tourdest.models import ShopPosition
from tourdest.models import Product
from tourdest.models import Payment
from tourdest.models import PaymentDetail

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
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.level = validated_data.get('level', instance.level)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

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
    user = UserSerializer()
    shop = ShopSerializer()

    def create(self, validated_data):
        return ShopPosition.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.shop = validated_data.get('shop', instance.shop)
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    shop = ShopSerializer()
    price = serializers.IntegerField()
    stock = serializers.IntegerField()
    status = serializers.BooleanField(default = False)
    description = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.shop = validated_data.get('shop', instance.shop)
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class PaymentSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    user = UserSerializer()
    shop = ShopSerializer()
    payment_type = serializers.ChoiceField(choices = [("CA", "Cash"), ("CR", "Credit"), ("DE", "Debit"), ("O", "Ovo"), ("G", "Gopay"), ("D", "Dana"),])
    total_price = serializers.IntegerField()
    payment_date = serializers.DateTimeField()
    status = serializers.ChoiceField(choices = [("P", "Paid"), ("NP", "Not Paid")])

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.shop = validated_data.get('shop', instance.shop)
        instance.payment_type = validated_data.get('payment_type', instance.payment_type)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class PaymentDetailSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    payment = PaymentSerializer()
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()

    def create(self, validated_data):
        return PaymentDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.payment = validated_data.get('payment', instance.payment)
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance