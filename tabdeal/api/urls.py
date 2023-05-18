from django.contrib import admin
from django.urls import path
from .views import SellerList, SellerDetail, Charge, Transfer
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('', SellerList.as_view()),
    path('<int:pk>/', SellerDetail.as_view()),
    path('charge/', Charge.as_view()),
    path('transfer/', Transfer.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]