from rest_framework import serializers
from tourdest.models import User
from tourdest.models import Shop
from tourdest.models import ShopPosition
from tourdest.models import Product
from tourdest.models import Payment
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
    user_id_input = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        user_id = validated_data.pop("user_id_input")
        validated_data["user_id"] = user_id
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        return ShopPosition.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_id = validated_data.pop("user_id_input", None)
        shop_id = self.initial_data.get("shop")
        if user_id:
            instance.user_id = user_id
        if shop_id:
            instance.shop_id = shop_id
        instance.save()
        return instance
    
    def save(self):
        # check if the instance already exists in the database
        if self.instance:
            # get the previous user from the database
            prev_user = self.instance.user
            # get the current user from the validated data
            user = User.objects.get(id=self.validated_data.get("user_id_input"))
            # update the status of the user if it has changed
            if user and user != prev_user:
                prev_user.status = False
                prev_user.save(update_fields=["status"])
                user.status = True
                user.save(update_fields=["status"])
        else:
            # get the user from the validated data
            user = User.objects.get(id=self.validated_data.get("user_id_input"))
            # set the status of the user to true for a new instance
            if user:
                user.status = True
                user.save(update_fields=["status"])
        # call the super method to save the instance
        return super().save()
    
    def delete(self):
        # get the shop position instance
        shop_position = self.get_object()
        # get the user from the instance
        user = shop_position.user
        # set the status of the user to false
        user.status = False
        user.save(update_fields=["status"])
        # call the super method to delete the instance
        super().delete()

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
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField()
    quantity_reject = serializers.IntegerField(default = 0)
    total_price = serializers.IntegerField()
    payment_date = serializers.DateTimeField(allow_null=True, required=False)
    status = serializers.ChoiceField(choices = [("P", "Paid"), ("NP", "Not Paid"), ("R", "Rejected")], default = "NP")
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        user_id = self.initial_data.get("user")
        validated_data["user_id"] = user_id
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        product_id = self.initial_data.get("product")
        validated_data["product_id"] = product_id
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user_id = self.initial_data.get("user")
        shop_id = self.initial_data.get("shop")
        product_id = self.initial_data.get("product")
        if user_id:
            instance.user_id = user_id
        if shop_id:
            instance.shop_id = shop_id
        if product_id:
            instance.product_id = product_id
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.quantity_reject = validated_data.get('quantity_reject', instance.quantity_reject)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)
        instance.status = validated_data.get('status', instance.status)
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