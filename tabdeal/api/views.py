from django.shortcuts import render
from sellers.serializers import SellerSerializer
from sellers.models import Seller
from rest_framework import generics


class SellerList(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    
class SellerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer