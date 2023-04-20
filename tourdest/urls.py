from django.urls import re_path
from tourdest import views

urlpatterns = [
    re_path(r'^tourdest/shop(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.shop_list),
    re_path(r'^tourdest/shop/(?P<pk>[0-9]+)(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.shop_detail),
    re_path(r'^tourdest/product/(?P<pk>[0-9]+)(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.product_detail),
    re_path(r'^tourdest/product(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?(?:/(?P<fk>[0-9]+))?/$', views.product_list),
    re_path(r'^tourdest/payment(?:/(?P<stat>\ball\b|\bpaid\b|\bnotpaid\b))?/$', views.payment_list),
    re_path(r'^tourdest/payment/(?P<pk>[0-9]+)(?:/(?P<stat>\ball\b|\bpaid\b|\bnotpaid\b))?/$', views.payment_detail),
    re_path(r'^tourdest/payment/get/(?P<stat>\ball\b|\bpaid\b|\bnotpaid\b)/(?P<user>[0-9]+)/(?P<shop>[0-9]+)/$', views.payment_get),
    re_path(r'^tourdest/paymentdet/$', views.paymentdet_list),
    re_path(r'^tourdest/paymentdet/get/(?P<payment>[0-9]+)/(?P<product>[0-9]+)/$', views.paymentdet_get),
    re_path(r'^tourdest/paymentdet/(?P<pk>[0-9]+)/$', views.paymentdet_detail),
]