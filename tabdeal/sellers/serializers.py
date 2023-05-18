from rest_framework import serializers
from .models import Seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('phone', 'wallet')
        model = Seller
        
class ChargeSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    
    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError('value must be positive')
        return value