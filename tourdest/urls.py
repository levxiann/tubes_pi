from django.urls import re_path
from tourdest import views
from django.contrib import admin

urlpatterns = [
    re_path(r'^tourdest/user(?:/(?P<lev>\ball\b|\bSA\b|\bA\b|\bE\b|\bC\b))?(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.user_list),
    re_path(r'^tourdest/user/(?P<pk>[0-9]+)/$', views.user_detail),
    re_path(r'^tourdest/user/create/$', views.user_create),
    re_path(r'^tourdest/user/login/$', views.user_login),
    re_path(r'^tourdest/user/logout/$', views.user_logout),
    re_path(r'^tourdest/shop(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.shop_list),
    re_path(r'^tourdest/shop/(?P<pk>[0-9]+)(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.shop_detail),
    re_path(r'^tourdest/shoppos/(?P<pk>[0-9]+)/$', views.shoppos_detail),
    re_path(r'^tourdest/shoppos/$', views.shoppos_list),
    re_path(r'^tourdest/shoppos/get/(?P<shop>[0-9]+)/$', views.shoppos_get),
    re_path(r'^tourdest/product/(?P<pk>[0-9]+)(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?/$', views.product_detail),
    re_path(r'^tourdest/product(?:/(?P<stat>\ball\b|\btrue\b|\bfalse\b))?(?:/(?P<fk>[0-9]+))?/$', views.product_list),
    re_path(r'^tourdest/payment(?:/(?P<stat>\ball\b|\bpaid\b|\bnotpaid\b))?/$', views.payment_list),
    re_path(r'^tourdest/payment/(?P<pk>[0-9]+)(?:/(?P<stat>\ball\b|\bpaid\b|\bnotpaid\b))?/$', views.payment_detail),
    re_path(r'^tourdest/payment/get/(?P<stat>\ball\b|\bpaid\b|\bnotpaid\b)/(?P<user>[0-9]+)/(?P<shop>[0-9]+)/$', views.payment_get),
    re_path(r'^tourdest/paymentdet/$', views.paymentdet_list),
    re_path(r'^tourdest/paymentdet/get/(?P<payment>[0-9]+)/(?P<product>[0-9]+)/$', views.paymentdet_get),
    re_path(r'^tourdest/paymentdet/(?P<pk>[0-9]+)/$', views.paymentdet_detail),
    re_path('admin/', admin.site.urls),
]