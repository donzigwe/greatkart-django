from django.contrib import admin
from .models import Payment, Order, OrderProduct


# Register your models here.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ['payment', 'user', 'product', 'product_price', 'quantity', 'is_ordered']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'order_number', 'email', 'phone_number', 'city', 'grand_total', 'tax', 'status',
                    'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone_number']
    list_per_page = 20
    search_help_text = 'Enter: Order ID, First Name, Last Name, Email or Phone Number'
    readonly_fields = ['order_number', ]
    inlines = [OrderProductInline, ]



admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)