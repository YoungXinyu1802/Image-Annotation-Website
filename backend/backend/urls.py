from django.urls import re_path, include
from . import views

urlpatterns = [
    re_path(r'login$', views.login),
    re_path(r'signup$', views.signup),
    re_path(r'label$', views.label),
    # re_path(r'show_users$', views.show_users, ),
]
