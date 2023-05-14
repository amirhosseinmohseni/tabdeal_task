from django.contrib import admin
from .models import Seller

class SellerAdmin(admin.ModelAdmin):
	list_display = ('phone', 'active', 'wallet')

	def active(self, obj):
		return obj.is_active == 1

	active.boolean = True

admin.site.register(Seller, SellerAdmin)
