from django.contrib import admin
from .models import Coupon, Newsletter, ContactMessage, Address

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    # 'discount' no existe en el modelo; usar 'discount_value' o definir un método
    list_display = ('code', 'discount_type', 'discount_value', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'phone', 'subject')
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'company', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone')
    search_fields = ('first_name', 'last_name', 'company', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone')  

