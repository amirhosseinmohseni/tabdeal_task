from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class SellerManager(BaseUserManager):
    
    def create_user(self, phone, password, wallet=0, **kwargs):
        if not phone:
            raise ValueError(_('The Phone must be set'))
        # if wallet < 0:
        #     raise ValueError(_('wallet must be greater than zero or zero'))
        # if not isinstance(wallet, int):
        #     raise ValueError(_('wallet value must be integer'))
        user = self.model(phone=phone, wallet=wallet, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, wallet,  **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(phone, password, **kwargs)