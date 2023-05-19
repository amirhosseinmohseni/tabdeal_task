from django.contrib import admin
from .models import Seller, Record

class SellerAdmin(admin.ModelAdmin):
	list_display = ('phone', 'active', 'wallet')

	def active(self, obj):
		return obj.is_active == 1

	active.boolean = True

admin.site.register(Seller, SellerAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = ('created', 'source_seller', 'type', 'destination_seller', 'amount')
    list_filter = ['created', 'source_seller', 'destination_seller', 'type']
    
admin.site.register(Record, RecordAdmin)