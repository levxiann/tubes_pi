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