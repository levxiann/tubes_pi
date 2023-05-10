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
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_list(request, lev = "all", stat = "all"):
    if request.method == 'GET':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
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
    elif request.method == 'POST':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        user_data = JSONParser().parse(request)
        user_data['status'] = False
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return JSONResponse({'data':user_serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_data['level'] = 'C'
        user_data['status'] = False
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return JSONResponse({'data':user_serializer.data, 'token': token.key}, status=status.HTTP_201_CREATED)
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserLoginSerializer(data=user_data)
        if user_serializer.is_valid():
            user = authenticate(request=request, username=user_data['username'], password=user_data['password'])
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return JSONResponse({'data': UserSerializer(user).data, 'token': token.key})
            else:
                return JSONResponse(user_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == "POST":
        request.user.auth_token.delete()

        logout(request)

        return JSONResponse("User Logout Successfully", status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        user_serializer = UserSerializer(user)
        return JSONResponse(user_serializer.data)

    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(user, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JSONResponse(user_serializer.data)
        return JSONResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shop_list(request, stat = "all"):
    if request.method == 'GET':
        if request.user.level != "C" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
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

    elif request.method == 'POST':
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shop_data = JSONParser().parse(request)
        shop_serializer = ShopSerializer(data=shop_data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shop_detail(request, pk, stat = "all"):
    try:
        if stat == "all":
            shop = Shop.objects.get(pk=pk)
        elif stat == "true":
            shop = Shop.objects.get(pk=pk, status = True)
        elif stat == "false":
            shop = Shop.objects.get(pk=pk, status = False)
    except Shop.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        shop_serializer = ShopSerializer(shop)
        return JSONResponse(shop_serializer.data)

    elif request.method == 'PUT':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shop_data = JSONParser().parse(request)
        shop_serializer = ShopSerializer(shop, data=shop_data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data)
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shop_data = JSONParser().parse(request)
        shop_serializer = ShopSerializer(shop, data=shop_data, partial=True)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data)
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shop.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shoppos_list(request):
    if request.method == 'GET':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos = ShopPosition.objects.all()
        shoppos_serializer = ShopPositionSerializer(shoppos, many=True)
        return JSONResponse(shoppos_serializer.data)

    elif request.method == 'POST':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos_data = JSONParser().parse(request)
        shoppos_serializer = ShopPositionSerializer(data=shoppos_data)
        if shoppos_serializer.is_valid():
            shoppos_serializer.save()
            return JSONResponse(shoppos_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(shoppos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shoppos_get(request, shop):
    if request.method == 'GET':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos = ShopPosition.objects.all().filter(shop_id = shop)
        shoppos_serializer = ShopPositionSerializer(shoppos, many=True)
        return JSONResponse(shoppos_serializer.data)
    
@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shoppos_get_user(request, user):
    if request.method == 'GET':
        if request.user.level == "C":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos = ShopPosition.objects.get(user_id = user)
        shoppos_serializer = ShopPositionSerializer(shoppos)
        return JSONResponse(shoppos_serializer.data)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def shoppos_detail(request, pk):
    try:
        shoppos = ShopPosition.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos_serializer = ShopPositionSerializer(shoppos)
        return JSONResponse(shoppos_serializer.data)

    elif request.method == 'PUT':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos_data = JSONParser().parse(request)
        shoppos_serializer = ShopPositionSerializer(shoppos, data=shoppos_data)
        if shoppos_serializer.is_valid():
            shoppos_serializer.save()
            return JSONResponse(shoppos_serializer.data)
        return JSONResponse(shoppos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos_data = JSONParser().parse(request)
        shoppos_serializer = ShopPositionSerializer(shoppos, data=shoppos_data, partial = True)
        if shoppos_serializer.is_valid():
            shoppos_serializer.save()
            return JSONResponse(shoppos_serializer.data)
        return JSONResponse(shoppos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        shoppos.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_list(request, stat = "all", fk = 0):
    if request.method == 'GET':
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

    elif request.method == 'POST':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_detail(request, pk, stat = "all"):
    try:
        if stat == "all":
            product = Product.objects.get(pk=pk)
        elif stat == "true":
            product = Product.objects.get(pk=pk, status = True)
        elif stat == "false":
            product = Product.objects.get(pk=pk, status = False)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        product_serializer = ProductSerializer(product)
        return JSONResponse(product_serializer.data)

    elif request.method == 'PUT':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(product, data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(product, data=product_data, partial = True)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user.level != "A" and request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    
@csrf_exempt
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_stock(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        if request.user.level != "A":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        product_data = JSONParser().parse(request)
        product.stock += product_data['stock']
        del product_data['stock']
        product_serializer = ProductSerializer(product, data=product_data, partial = True)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_list(request, stat = "all"):
    if request.method == 'GET':
        if request.user.level != "SA":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
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

    elif request.method == 'POST':
        if request.user.level != "C":
            return JSONResponse({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)
        payment_data = JSONParser().parse(request)
        payment_data['quantity_reject'] = 0
        payment_data['status'] = 'NP'
        payment_serializer = PaymentSerializer(data=payment_data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_detail(request, pk, stat = "all"):
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

    if request.method == 'GET':
        payment_serializer = PaymentSerializer(payment)
        return JSONResponse(payment_serializer.data)

    elif request.method == 'PUT':
        payment_data = JSONParser().parse(request)
        payment_serializer = PaymentSerializer(payment, data=payment_data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data)
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        payment_data = JSONParser().parse(request)
        payment_serializer = PaymentSerializer(payment, data=payment_data, partial = True)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data)
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product = payment.product
        product.stock += payment.quantity
        product.save()
        payment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def payment_get(request, user, shop, stat = "all"):
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