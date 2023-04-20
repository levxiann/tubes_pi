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
from tourdest.models import PaymentDetail
from tourdest.serializers import UserSerializer
from tourdest.serializers import ShopSerializer
from tourdest.serializers import ShopPositionSerializer
from tourdest.serializers import ProductSerializer
from tourdest.serializers import PaymentSerializer
from tourdest.serializers import PaymentDetailSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def shop_list(request, stat = "all"):
    if request.method == 'GET':
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
        shop_data = JSONParser().parse(request)
        shop_serializer = ShopSerializer(data=shop_data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
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
        shop_data = JSONParser().parse(request)
        shop_serializer = ShopSerializer(shop, data=shop_data)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data)
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        shop_data = JSONParser().parse(request)
        shop_serializer = ShopSerializer(shop, data=shop_data, partial=True)
        if shop_serializer.is_valid():
            shop_serializer.save()
            return JSONResponse(shop_serializer.data)
        return JSONResponse(shop_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        shop.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def product_list(request, stat = "all", fk = 0):
    if request.method == 'GET':
        if stat == "all":
            if fk == 0 :
                products = Product.objects.all()
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
            else :
                products = Product.objects.all().filter(shop_id = fk)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
        elif stat == "true":
            if fk == 0:
                products = Product.objects.all().filter(status = True)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
            else :
                products = Product.objects.all().filter(status = True, shop_id = fk)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
        elif stat == "false":
            if fk == 0 :
                products = Product.objects.all().filter(status = False)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)
            else :
                products = Product.objects.all().filter(status = False, shop_id = fk)
                products_serializer = ProductSerializer(products, many=True)
                return JSONResponse(products_serializer.data)

    elif request.method == 'POST':
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
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
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(product, data=product_data)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        product_data = JSONParser().parse(request)
        product_serializer = ProductSerializer(product, data=product_data, partial = True)
        if product_serializer.is_valid():
            product_serializer.save()
            return JSONResponse(product_serializer.data)
        return JSONResponse(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def payment_list(request, stat = "all"):
    if request.method == 'GET':
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

    elif request.method == 'POST':
        payment_data = JSONParser().parse(request)
        payment_serializer = PaymentSerializer(data=payment_data)
        if payment_serializer.is_valid():
            payment_serializer.save()
            return JSONResponse(payment_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(payment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def payment_detail(request, pk, stat = "all"):
    try:
        if stat == "all":
            payment = Payment.objects.get(pk=pk)
        elif stat == "paid":
            payment = Payment.objects.get(pk=pk, status = "P")
        elif stat == "notpaid":
            payment = Payment.objects.get(pk=pk, status = "NP")
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
        payment.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
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

@csrf_exempt
def paymentdet_list(request):
    if request.method == 'POST':
        paymentdet_data = JSONParser().parse(request)
        paymentdet_serializer = PaymentDetailSerializer(data=paymentdet_data)
        if paymentdet_serializer.is_valid():
            paymentdet_serializer.save()
            return JSONResponse(paymentdet_serializer.data, status=status.HTTP_201_CREATED)
        return JSONResponse(paymentdet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def paymentdet_get(request, payment, product):
    if request.method == 'GET':
        if payment == "0":
            if product == "0":
                paymentdets = PaymentDetail.objects.all()
                paymentdets_serializer = PaymentDetailSerializer(paymentdets, many=True)
                return JSONResponse(paymentdets_serializer.data)
            else:
                paymentdets = PaymentDetail.objects.all().filter(product_id = product)
                paymentdets_serializer = PaymentDetailSerializer(paymentdets, many=True)
                return JSONResponse(paymentdets_serializer.data)
        else:
            if product == "0":
                paymentdets = PaymentDetail.objects.all().filter(payment_id = payment)
                paymentdets_serializer = PaymentDetailSerializer(paymentdets, many=True)
                return JSONResponse(paymentdets_serializer.data)
            else:
                paymentdets = PaymentDetail.objects.all().filter(product_id = product, payment_id = payment)
                paymentdets_serializer = PaymentDetailSerializer(paymentdets, many=True)
                return JSONResponse(paymentdets_serializer.data)

@csrf_exempt
def paymentdet_detail(request, pk):
    try:
        paymentdet = PaymentDetail.objects.get(pk=pk)
    except PaymentDetail.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        paymentdet_serializer = PaymentDetailSerializer(paymentdet)
        return JSONResponse(paymentdet_serializer.data)

    elif request.method == 'PUT':
        paymentdet_data = JSONParser().parse(request)
        paymentdet_serializer = PaymentDetailSerializer(paymentdet, data=paymentdet_data)
        if paymentdet_serializer.is_valid():
            paymentdet_serializer.save()
            return JSONResponse(paymentdet_serializer.data)
        return JSONResponse(paymentdet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        paymentdet_data = JSONParser().parse(request)
        paymentdet_serializer = PaymentDetailSerializer(paymentdet, data=paymentdet_data, partial = True)
        if paymentdet_serializer.is_valid():
            paymentdet_serializer.save()
            return JSONResponse(paymentdet_serializer.data)
        return JSONResponse(paymentdet_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product = paymentdet.product
        product.stock += paymentdet.quantity
        product.save()
        paymentdet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)