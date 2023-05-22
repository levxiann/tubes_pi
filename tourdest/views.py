from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import status
from tourdest.models import User
from tourdest.models import Shop
from tourdest.models import ShopPosition
from tourdest.models import Product
from tourdest.models import Payment
from tourdest.serializers import UserSerializer
from tourdest.serializers import UserLoginSerializer
from tourdest.serializers import ShopSerializer
from tourdest.serializers import ShopPositionSerializer
from tourdest.serializers import ProductSerializer
from tourdest.serializers import PaymentSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import logout

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        # mengembalikan data dalam bentuk json
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya menerima GET dan POST
@authentication_classes([TokenAuthentication]) # memastikan user memiliki token yang valid sebelum mengakses resource
@permission_classes([IsAuthenticated]) # memastika user telah terautentikasi
def user_list(request, lev = "all", stat = "all"):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ambil data dari tabel user sesuai dengan status dan level, kembalikan dalam bentuk json
        if stat == "all":
            if lev == "all":
                users = User.objects.all()
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
            else:
                users = User.objects.all().filter(level = lev)
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
        elif stat == "true":
            if lev == "all":
                users = User.objects.all().filter(status = True)
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
            else:
                users = User.objects.all().filter(status = True, level = lev)
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
        elif stat == "false":
            if lev == "all":
                users = User.objects.all().filter(status = False)
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
            else:
                users = User.objects.all().filter(status = False, level = lev)
                users_serializer = UserSerializer(users, many=True)
                return JSONResponse(users_serializer.data)
    # jika request method POST (create user oleh admin dan super admin)
    elif request.method == 'POST':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # status default false ketika user dibuat (tidak bekerja)
        user_data['status'] = False
        # validasi data user
        user_serializer = UserSerializer(data=user_data)
        # jika valid, simpan user ke tabel user
        if user_serializer.is_valid():
            user = user_serializer.save()
            return JSONResponse({'data':user_serializer.data}, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def user_create(request):
    # jika request method POST (registrasi)
    if request.method == 'POST':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # level default Customer ketika registrasi
        user_data['level'] = 'C'
        # status default false ketika user dibuat (tidak bekerja)
        user_data['status'] = False
        # validasi data user
        user_serializer = UserSerializer(data=user_data)
        # jika valid, simpan user ke tabel user dan buat access token
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return JSONResponse({'data':user_serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def user_login(request):
    # jika request method POST (login)
    if request.method == 'POST':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # validasi data user
        user_serializer = UserLoginSerializer(data=user_data)
        # jika valid, cek apakah user dan password sesuai dengan yang ada di tabel user
        if user_serializer.is_valid():
            user = authenticate(request=request, username=user_data['username'], password=user_data['password'])
            # Jika ya, buat access token
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return JSONResponse({'data': UserSerializer(user).data, 'token': token.key})
            else:
                # Jika tidak kembalikan response 401
                return JSONResponse(user_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        # Jika tidak valid, kembalikan response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST']) # hanya menerima method POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user yang terautentikasi yang bisa akses
def user_logout(request):
    # jika request method POST (logout)
    if request.method == "POST":
        # hapus access token user
        request.user.auth_token.delete()

        # logout user
        logout(request)

        # return response 200
        return JSONResponse("User Logout Successfully", status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya menerima method GET, PUT, PATCH, DELETE
@authentication_classes([TokenAuthentication]) # Autentikasi token
@permission_classes([IsAuthenticated]) # Hanya user terautentikasi yang bisa akses
def user_detail(request, pk):
    # ambil data user sesuai primary key
    try:
        user = User.objects.get(pk=pk)
    # return response 404 jika user tidak ada
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # validasi data user
        user_serializer = UserSerializer(user)
        # kembalikan dalam bentuk json
        return JSONResponse(user_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # validasi data user
        user_serializer = UserSerializer(user, data=user_data)
        # jika valid simpan data user baru
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # mengubah data json dari request body menjadi dictionary
        user_data = JSONParser().parse(request)
        # validasi data user
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        # jika valid simpan data user baru
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus user
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya method GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def shop_list(request, stat = "all"):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level customer dan super admin, kembalikan response 403
        if request.user.level != "C" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # mengambil data berdasarkan status
        if stat == "all":
            shops = Shop.objects.all()
            shops_serializer = ShopSerializer(shops, many=True)
            return JSONResponse(shops_serializer.data)
        elif stat == "true":
            shops = Shop.objects.all().filter(status = True)
            shops_serializer = ShopSerializer(shops, many=True)
            return JSONResponse(shops_serializer.data)
        elif stat == "false":
            shops = Shop.objects.all().filter(status = False)
            shops_serializer = ShopSerializer(shops, many=True)
            return JSONResponse(shops_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level super admin, kembalikan response 403
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        shop_data = JSONParser().parse(request)
        # validasi data toko
        shop_serializer = ShopSerializer(data=shop_data)
        # jika valid simpan data
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # menerima method GET, PUT, PATCH, DELETE
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang punya akses
def shop_detail(request, pk, stat = "all"):
    # ambil data sesuai id dan status
    try:
        if stat == "all":
            shop = Shop.objects.get(pk=pk)
        elif stat == "true":
            shop = Shop.objects.get(pk=pk, status = True)
        elif stat == "false":
            shop = Shop.objects.get(pk=pk, status = False)
    except Shop.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # validasi data toko dan return data toko
        shop_serializer = ShopSerializer(shop)
        return JSONResponse(shop_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        shop_data = JSONParser().parse(request)
        # validasi data toko
        shop_serializer = ShopSerializer(shop, data=shop_data)
        # jika valid simpan data
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        shop_data = JSONParser().parse(request)
        # validasi data toko
        shop_serializer = ShopSerializer(shop, data=shop_data, partial=True)
        # jika valid simpan data
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level super admin, kembalikan response 403
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus data
        shop.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST']) # methog GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang punya akses
def shoppos_list(request):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ambil data posisi toko dan return dalam bentuk json
        shoppos = ShopPosition.objects.all()
        # validasi data posisi toko
        shoppos_serializer = ShopPositionSerializer(shoppos, many=True)
        return JSONResponse(shoppos_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        shoppos_data = JSONParser().parse(request)
        # validasi data posisi toko
        shoppos_serializer = ShopPositionSerializer(data=shoppos_data)
        # jika valid simpan data
        if shoppos_serializer.is_valid():
            shoppos_serializer.save()
            return JSONResponse(shoppos_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(shoppos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET']) # hanya method GET
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang dapat akses
def shoppos_get(request, shop):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ambil data posisi toko berdasarkan toko dan return dalam bentuk json
        shoppos = ShopPosition.objects.all().filter(shop_id = shop)
        shoppos_serializer = ShopPositionSerializer(shoppos, many=True)
        return JSONResponse(shoppos_serializer.data)
    
@csrf_exempt
@api_view(['GET']) # hanya method GET
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def shoppos_get_user(request, user):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses adalah level customer, kembalikan response 403
        if request.user.level == "C":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ambil data posisi toko tertentu berdasarkan id user dan return bentuk json
        shoppos = ShopPosition.objects.get(user_id = user)
        shoppos_serializer = ShopPositionSerializer(shoppos)
        return JSONResponse(shoppos_serializer.data)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya method GET, PUT, PATCH, DELETE
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shoppos_detail(request, pk):
    # ambil data posisi toko berdasarkan primary key
    try:
        shoppos = ShopPosition.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # return data posisi toko dalam bentuk json
        shoppos_serializer = ShopPositionSerializer(shoppos)
        return JSONResponse(shoppos_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        shoppos_data = JSONParser().parse(request)
        # validasi data posisi toko
        shoppos_serializer = ShopPositionSerializer(shoppos, data=shoppos_data)
        # jika valid simpan data
        if shoppos_serializer.is_valid():
            shoppos_serializer.save()
            return JSONResponse(shoppos_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(shoppos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        shoppos_data = JSONParser().parse(request)
        # validasi data posisi toko
        shoppos_serializer = ShopPositionSerializer(shoppos, data=shoppos_data, partial = True)
        # jika valid simpan data
        if shoppos_serializer.is_valid():
            shoppos_serializer.save()
            return JSONResponse(shoppos_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(shoppos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # tambah stock pada tabel product jika data transaksi dihapus
        user = shoppos.user
        user.status = False
        user.save()

        # hapus data
        shoppos.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST']) # hanya method GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def product_list(request, stat = "all", fk = 0):
    # jika request method GET
    if request.method == 'GET':
        # ambil data produk berdasarkan status atau toko 
        if stat == "all":
            if fk == "0" :
                products = Product.objects.all()
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
            else :
                products = Product.objects.all().filter(shop_id = fk)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
        elif stat == "true":
            if fk == "0":
                products = Product.objects.all().filter(status = True)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
            else :
                products = Product.objects.all().filter(status = True, shop_id = fk)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
        elif stat == "false":
            if fk == "0" :
                products = Product.objects.all().filter(status = False)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
            else :
                products = Product.objects.all().filter(status = False, shop_id = fk)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level admin, kembalikan response 403
        if request.user.level != "A":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        product_data = JSONParser().parse(request)
        # validasi data produk
        product_serializer = ProductSerializer(data=product_data)
        # jika valid simpan data
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya method GET, PUT, PATCH, DELETE
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def product_detail(request, pk, stat = "all"):
    # ambil data produk tertentu berdasarkan primary key dan status
    try:
        if stat == "all":
            product = Product.objects.get(pk=pk)
        elif stat == "true":
            product = Product.objects.get(pk=pk, status = True)
        elif stat == "false":
            product = Product.objects.get(pk=pk, status = False)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # return data produk dalam bentuk json
        product_serializer = ProductSerializer(product)
        return JSONResponse(product_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        product_data = JSONParser().parse(request)
        # validasi data produk
        product_serializer = ProductSerializer(product, data=product_data)
        # jika valid simpan data
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        product_data = JSONParser().parse(request)
        # validasi data produk
        product_serializer = ProductSerializer(product, data=product_data, partial = True)
        # jika valid simpan data
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Jika request method DELETE
    elif request.method == 'DELETE':
        # apabila yang mengakses bukan level admin dan super admin, kembalikan response 403
        if request.user.level != "A":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # hapus data produk
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['PATCH']) # hanya untuk method PATCH
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def product_stock(request, pk):
    # ambil data produk tertentu berdasarkan primary key
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method PATCH
    if request.method == 'PATCH':
        # apabila yang mengakses bukan level admin, kembalikan response 403
        if request.user.level != "A":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        product_data = JSONParser().parse(request)
        # stok produk ditambah sesuai dengan request body
        product.stock += product_data['stock']
        # hapus data stock dari request
        del product_data['stock']
        # validasi data produk
        product_serializer = ProductSerializer(product, data=product_data, partial = True)
        # jika valid simpan data
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'POST']) # hanya method GET dan POST
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def payment_list(request, stat = "all"):
    # jika request method GET
    if request.method == 'GET':
        # apabila yang mengakses bukan level super admin, kembalikan response 403
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ambil data transaksi berdasarkan status
        if stat == "all":
            payments = Payment.objects.all()
            payments_serializer = PaymentSerializer(payments, many=True)
            return JSONResponse(payments_serializer.data)
        elif stat == "paid":
            payments = Payment.objects.all().filter(status = "P")
            payments_serializer = PaymentSerializer(payments, many=True)
            return JSONResponse(payments_serializer.data)
        elif stat == "notpaid":
            payments = Payment.objects.all().filter(status = "NP")
            payments_serializer = PaymentSerializer(payments, many=True)
            return JSONResponse(payments_serializer.data)
        elif stat == "rejected":
            payments = Payment.objects.all().filter(status = "R")
            payments_serializer = PaymentSerializer(payments, many=True)
            return JSONResponse(payments_serializer.data)

    # jika request method POST
    elif request.method == 'POST':
        # apabila yang mengakses bukan level customer, kembalikan response 403
        if request.user.level != "C":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        # ubah data json menjadi dictionary
        payment_data = JSONParser().parse(request)
        # quantity_reject default 0
        payment_data['quantity_reject'] = 0
        # status pembayaran default not paid
        payment_data['status'] = 'NP'
        # validasi data payment
        payment_serializer = PaymentSerializer(data=payment_data)
        # jika valid simpan data
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data, status=status.HTTP_201_CREATED)
        # jika tidak valid, return response 400
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE']) # hanya method GET, PUT, PATCH, DELETE
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def payment_detail(request, pk, stat = "all"):
    # ambil data payment tertentu berdasarkan primary key dan status
    try:
        if stat == "all":
            payment = Payment.objects.get(pk=pk)
        elif stat == "paid":
            payment = Payment.objects.get(pk=pk, status = "P")
        elif stat == "notpaid":
            payment = Payment.objects.get(pk=pk, status = "NP")
        elif stat == "rejected":
            payment = Payment.objects.get(pk=pk, status = "R")
    except Payment.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    # jika request method GET
    if request.method == 'GET':
        # return data payment dalam bentuk json
        payment_serializer = PaymentSerializer(payment)
        return JSONResponse(payment_serializer.data)

    # jika request method PUT
    elif request.method == 'PUT':
        # ubah data json menjadi dictionary
        payment_data = JSONParser().parse(request)
        # validasi data payment
        payment_serializer = PaymentSerializer(payment, data=payment_data)
        # jika valid simpan data
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method PATCH
    elif request.method == 'PATCH':
        # ubah data json menjadi dictionary
        payment_data = JSONParser().parse(request)
        # validasi data payment
        payment_serializer = PaymentSerializer(payment, data=payment_data, partial = True)
        # jika valid simpan data
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data)
        # jika tidak valid, return response 400
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # jika request method DELETE
    elif request.method == 'DELETE':
        # tambah stock pada tabel product jika data transaksi dihapus
        product = payment.product
        product.stock += payment.quantity
        product.save()
        # hapus data transaksi
        payment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET']) # hanya method GET
@authentication_classes([TokenAuthentication]) # autentikasi token
@permission_classes([IsAuthenticated]) # hanya user terautentikasi yang bisa akses
def payment_get(request, user, shop, stat = "all"):
    # ambil data payment berdasarkan user atau toko atau status dan return data dalam bentuk json
    if request.method == 'GET':
        if stat == "all":
            if user == "0":
                if shop == "0":
                    payments = Payment.objects.all()
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop)
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
            else:
                if shop == "0":
                    payments = Payment.objects.all().filter(user_id = user)
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, user_id = user)
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
        elif stat == "paid":
            if user == "0":
                if shop == "0":
                    payments = Payment.objects.all().filter(status = "P")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, status = "P")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
            else:
                if shop == "0":
                    payments = Payment.objects.all().filter(user_id = user, status = "P")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, user_id = user, status = "P")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
        elif stat == "notpaid":
            if user == "0":
                if shop == "0":
                    payments = Payment.objects.all().filter(status = "NP")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, status = "NP")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
            else:
                if shop == "0":
                    payments = Payment.objects.all().filter(user_id = user, status = "NP")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, user_id = user, status = "NP")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
        elif stat == "rejected":
            if user == "0":
                if shop == "0":
                    payments = Payment.objects.all().filter(status = "R")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, status = "R")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
            else:
                if shop == "0":
                    payments = Payment.objects.all().filter(user_id = user, status = "R")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)
                else:
                    payments = Payment.objects.all().filter(shop_id = shop, user_id = user, status = "R")
                    payments_serializer = PaymentSerializer(payments, many=True)
                    return JSONResponse(payments_serializer.data)