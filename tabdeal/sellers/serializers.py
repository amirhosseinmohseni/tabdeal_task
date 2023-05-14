from rest_framework import serializers
from .models import Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('phone', 'wallet')
        model = Seller