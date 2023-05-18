from django.shortcuts import render
from sellers.serializers import SellerListSerializer, SellerDetailSerializer, ChargeSerializer, TransferSerializer
from sellers.models import Seller, Record
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.core import serializers
from sellers.permission import IsOwner
from django.db import transaction



class SellerListView(generics.ListAPIView):
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Seller.objects.all()
    serializer_class = SellerListSerializer
    
    # def get(self, request, *args, **kwargs):
    #     data = Seller.objects.all()
    #     json = SellerListSerializer(data, many=True)
    #     content = {
    #         'user': str(request.user),
    #         'access_token': str(request.auth),
    #     }        
    #     return Response(content)
            
class SellerDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        phone = request.user.phone
        wallet = Seller.objects.get(phone=phone).wallet
        content = {
            'user': str(phone),
            'wallet': wallet
        }
        return Response(content)

# class SellerDetail(generics.GenericAPIView):
#     serializer_class
    
class Charge(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ChargeSerializer(data=request.data)
        if serializer.is_valid():
            seller = Seller.objects.get(phone=request.user.phone)
            seller.wallet += serializer.data['value']
            seller.save()
            record = Record(source_seller=Seller.objects.get(phone=request.user),
                            destination_seller=None,
                            type='charge',
                            amount=serializer.data['value'])
            record.save()
            content = {
                'user': request.user.phone,
                'wallet': Seller.objects.get(phone=request.user.phone).wallet
            }
            return Response(content)
        return Response(serializer.errors)
        
class Transfer(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = TransferSerializer(context = {"user": request.user.phone}, data=request.data)
        if serializer.is_valid():
            amount = Seller.objects.get(phone=request.user.phone).wallet
            value = serializer.data['value']
            dest = Seller.objects.get(phone=serializer.data['phone'])
            source = Seller.objects.get(phone=request.user.phone)
            source.wallet -= value
            dest.wallet += value
            source.save()
            dest.save()
            record = Record(source_seller=source,
                            destination_seller=dest,
                            type='transfer',
                            amount=value)
            record.save()
            content = {
                'source': request.user.phone,
                'source_wallet': Seller.objects.get(phone=request.user.phone).wallet,
                'destination': serializer.data['phone'],
                'value': Seller.objects.get(phone=serializer.data['phone']).wallet
            }
            return Response(content)
        return Response(serializer.errors)