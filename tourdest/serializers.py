from rest_framework import serializers
from tourdest.models import User
from tourdest.models import Shop
from tourdest.models import ShopPosition
from tourdest.models import Product
from tourdest.models import Payment
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100, allow_null=True)
    phone_number = serializers.CharField(max_length=20)
    level = serializers.ChoiceField(choices = [("SA", "Super Admin"), ("A", "Admin"), ("E", "Employee"), ("C", "Customer"),], default = "C")
    status = serializers.BooleanField(default = False)

    # fungsi ketika melakukan CREATE
    def create(self, validated_data):
        # menyimpan password ke dalam sebuah variabel password
        password = validated_data.pop('password', None)
        # jika password ada (tidak kosong)
        if password is not None:
            # password dihash sebelum disimpan ke tabel
            validated_data['password'] = make_password(password)
        # Simpan ke tabel user
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # mengupdate semua data - data menjadi data yang baru
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data.get('password', None)
        # Jika password tidak kosong
        if password is not None:
            # hash password yang baru dan simpan
            instance.password = make_password(password)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.level = validated_data.get('level', instance.level)
        instance.status = validated_data.get('status', instance.status)
        # update ke tabel user
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    # validasi data - data yang akan digunakan untuk login
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100, write_only=True)

class ShopSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel shop
    name = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=255)
    status = serializers.BooleanField(default = False)

    def create(self, validated_data):
        # Menyimpan data yang valid ke tabel shop
        return Shop.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Mengganti data lama dengan data baru yang sudah valid
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        # Menyimpan data baru ke tabel shop
        instance.save()
        return instance

class ShopPositionSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel shop
    # validasi foreign key user ke UserSerializer
    user = UserSerializer(read_only = True)
    # validasi foreign key shop ke ShopSerializer
    shop = ShopSerializer(read_only = True)
    # write only berarti hanya untuk dibaca dan tidak akan dikembalikan pada response
    user_id_input = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        # menghapus user_id_input dari data yang akan disimpan ke tabel dan menyimpan valuenya ke variabel user_id
        user_id = validated_data.pop("user_id_input")
        # kolom user_id disimpan dengan data dari user_id_input
        validated_data["user_id"] = user_id
        # menyimpan data dari shop (id) ke kolom shop_id pada data yang divalidasi
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        # menyimpan data ke tabel shop position
        return ShopPosition.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # menghapus user_id_input dari data yang akan disimpan ke tabel dan menyimpan valuenya ke variabel user_id
        user_id = validated_data.pop("user_id_input", None)
        # menyimpan data dari shop (id) ke kolom shop_id pada data yang divalidasi
        shop_id = self.initial_data.get("shop")
        # update data user apabila ada pada request body
        if user_id:
            instance.user_id = user_id
        # update data toko apabila ada pada request body
        if shop_id:
            instance.shop_id = shop_id
        # menyimpan data baru ke tabel shop position
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
                # status user sebelumnya menjadi false (tidak bekerja)
                prev_user.status = False
                prev_user.save(update_fields=["status"])
                # status user baru menjadi true (bekerja)
                user.status = True
                user.save(update_fields=["status"])
        else:
            # get the user from the validated data
            user = User.objects.get(id=self.validated_data.get("user_id_input"))
            # set the status of the user to true for a new instance
            if user:
                # status user baru menjadi true
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
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel shop
    name = serializers.CharField(max_length=100)
    # validasi foreign key shop ke ShopSerializer
    shop = ShopSerializer(read_only = True)
    price = serializers.IntegerField()
    stock = serializers.IntegerField()
    status = serializers.BooleanField(default = False)
    description = serializers.CharField(max_length=255)

    def create(self, validated_data):
        # menyimpan data dari shop (id) ke kolom shop_id pada data yang divalidasi
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        # menyimpan data produk ke tabel product
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # menyimpan data dari shop (id) ke kolom shop_id pada data yang divalidasi
        shop_id = self.initial_data.get("shop")
        # menyimpan data baru yang divalidasi ke data lama
        instance.name = validated_data.get('name', instance.name)
        # update data shop_id jika ada pada request body
        if shop_id:
            instance.shop_id = shop_id
        instance.price = validated_data.get('price', instance.price)
        instance.stock = validated_data.get('stock', instance.stock)
        instance.status = validated_data.get('status', instance.status)
        instance.description = validated_data.get('description', instance.description)
        # menyimpan data baru ke tabel product
        instance.save()
        return instance

class PaymentSerializer(serializers.Serializer):
    # id tidak akan diubah (read only)
    pk = serializers.IntegerField(read_only=True)
    # validasi data - data yang akan disimpan ke tabel shop
    # validasi foreign key user ke UserSerializer
    user = UserSerializer(read_only=True)
    # validasi foreign key shop ke ShopSerializer
    shop = ShopSerializer(read_only=True)
    # validasi foreign key product ke ProductSerializer
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField()
    quantity_reject = serializers.IntegerField(default = 0)
    total_price = serializers.IntegerField()
    payment_date = serializers.DateTimeField(allow_null=True, required=False)
    status = serializers.ChoiceField(choices = [("P", "Paid"), ("NP", "Not Paid"), ("R", "Rejected")], default = "NP")
    # created tidak akan diubah (read only)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        # menyimpan data dari user (id) ke kolom user_id pada data yang divalidasi
        user_id = self.initial_data.get("user")
        validated_data["user_id"] = user_id
        # menyimpan data dari shop (id) ke kolom shop_id pada data yang divalidasi
        shop_id = self.initial_data.get("shop")
        validated_data["shop_id"] = shop_id
        # menyimpan data dari product (id) ke kolom product_id pada data yang divalidasi
        product_id = self.initial_data.get("product")
        validated_data["product_id"] = product_id
        # menyimpan data yang tervalidasi ke tabel payment
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # menyimpan data dari user (id) ke kolom user_id pada data yang divalidasi
        user_id = self.initial_data.get("user")
        # menyimpan data dari shop (id) ke kolom shop_id pada data yang divalidasi
        shop_id = self.initial_data.get("shop")
        # menyimpan data dari product (id) ke kolom product_id pada data yang divalidasi
        product_id = self.initial_data.get("product")
        # update data user_id jika ada pada request body
        if user_id:
            instance.user_id = user_id
        # update data shop_id jika ada pada request body
        if shop_id:
            instance.shop_id = shop_id
        # update data product_id jika ada pada request body
        if product_id:
            instance.product_id = product_id
        # simpan data baru yang tervalidasi ke data lama
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.quantity_reject = validated_data.get('quantity_reject', instance.quantity_reject)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.payment_date = validated_data.get('payment_date', instance.payment_date)
        instance.status = validated_data.get('status', instance.status)
        # meyimpan data baru ke tabel payment
        instance.save()
        return instance

    def save(self):
        if self.instance:
            # apabila data diupdate, stock pada tabel product akan dikurang atau ditambah sesuai dengan data baru
            previous_quantity = self.instance.quantity
            prev_product = self.instance.product
            instance = super().save()
            product = instance.product
            prev_product.stock += previous_quantity
            prev_product.save()
            product.stock -= instance.quantity
        else:
            # apabila data dicreate, stock pada tabel product akan dikurang sesuai dengan jumlah quantity
            instance = super().save()
            product = instance.product
            product.stock -= instance.quantity
        product.save()
        return instance