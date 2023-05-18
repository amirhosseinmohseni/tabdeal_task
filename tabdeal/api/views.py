from django.shortcuts import render
from sellers.serializers import SellerSerializer, ChargeSerializer
from sellers.models import Seller
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core import serializers
from sellers.permission import IsOwner
from django.db import transaction



class SellerList(generics.ListAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    
    def get(self, request, *args, **kwargs):
        data = Seller.objects.all()
        json = SellerSerializer(data, many=True)
        content = {
            'user': str(request.user),
            'access_token': str(request.auth),
            # 'list': str(json)
        }        
        return Response(content)
            
class SellerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner, )
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    
class Charge(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ChargeSerializer(data=request.data)
        if serializer.is_valid():
            seller = Seller.objects.get(phone=request.user.phone)
            seller.wallet += serializer.data['value']
            seller.save()
            content = {
                'user': request.user.phone,
                'wallet': request.user.wallet
            }
            return Response(content)
        return Response(serializer.errors)
        