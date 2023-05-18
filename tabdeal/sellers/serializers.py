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
    
class TransferSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    value = serializers.IntegerField()
    
    def validate_phone(self, data):
        sellers = list(Seller.objects.all().values_list('phone', flat=True))
        if data not in sellers:
            raise serializers.ValidationError('user not found')
        if data == self.context['user']:
            raise serializers.ValidationError("you can't transfer to your account")
        return data
    
    def validate_value(self, data):
        if data <= 0:
            raise serializers.ValidationError('value must be positive')
        if data >= Seller.objects.get(phone=self.context['user']).wallet:
            raise serializers.ValidationError('value is greater than walet')
        return data