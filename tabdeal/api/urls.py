from django.contrib import admin
from django.urls import path
from .views import SellerList, SellerDetail

urlpatterns = [
    path('', SellerList.as_view()),
    path('<int:pk>/', SellerDetail.as_view()),

]