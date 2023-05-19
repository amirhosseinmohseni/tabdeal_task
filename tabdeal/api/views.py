from django.shortcuts import render
from sellers.serializers import SellerListSerializer, SellerDetailSerializer, ChargeSerializer, TransferSerializer, RegisterSerializer
from sellers.models import Seller, Record
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.core import serializers
from sellers.permission import IsOwner
from django.db import transaction


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            seller = serializer.save()
        return Response({
            "user": RegisterSerializer(seller, context=self.get_serializer_context()).data
        })

class SellerListView(generics.ListAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerListSerializer
            
class SellerDetailView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        phone = request.user.phone
        wallet = Seller.objects.get(phone=phone).wallet
        print(request.auth)
        content = {
            'user': str(phone),
            'wallet': wallet
        }
        return Response(content)
    
class Charge(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ChargeSerializer(data=request.data)
        if serializer.is_valid():
            seller = Seller.objects.get(phone=request.user.phone)
            amount = serializer.data['value']
            seller.wallet += amount
            seller.save()
            record = Record(source_seller=seller,
                            destination_seller=None,
                            type='charge',
                            amount=amount)
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
                'destination': serializer.data['phone']
            }
            return Response(content)
        return Response(serializer.errors)