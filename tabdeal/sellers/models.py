from django.db import models
from .managers import SellerManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Seller(AbstractUser):
    username = None
    phone = models.CharField(_("phone number"), max_length=11, unique=True)
    wallet = models.PositiveBigIntegerField()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    objects = SellerManager()
    
    def __str__(self):
        return self.phone