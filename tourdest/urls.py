from django.urls import re_path
from tourdest import views

urlpatterns = [
    re_path(r'^tourdest/$', views.game_list),
    re_path(r'^tourdest/(?P<pk>[0-9]+)/$', views.game_detail),
]