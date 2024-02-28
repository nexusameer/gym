from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('service',views.service, name='service'),
    path('buyplan',views.buyplan, name='buyplan'),
    path('viewplan',views.viewplan, name='viewplan'),
    path('success_page/', views.success_page, name='success_page'), 


    # Authentications
    path('loginuser/',views.loginuser, name='loginuser'),
    path('logoutuser/',views.logoutuser, name='logoutuser'),
    path('registeruser/',views.registeruser, name='registeruser'),
]
