from django.db import models
from .managers import SellerManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


TYPE_CHOICES = [
    ('charge', 'CHARGE'),
    ('transfer', 'TRANSFER')
]

class Seller(AbstractUser):
    username = None
    phone = models.CharField(_("phone number"), max_length=11, unique=True)
    wallet = models.PositiveBigIntegerField()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = SellerManager()
    
    def __str__(self):
        return self.phone
    
class Record(models.Model):
    source_seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='source_seller')
    destination_seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, related_name='destination_seller')
    amount = models.PositiveBigIntegerField()
    type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.type == 'charge':
            return f"at {self.created}: {self.source_seller} charged {self.amount}"
        else:
            return f"at {self.created}: {self.source_seller} transfered {self.amount} to {self.destination_seller}"