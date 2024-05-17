from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class AccountAdmin(UserAdmin):
    list_display = ['first_name', 'last_name', 'email','username', 'phone_number', 'is_active', 'last_login', 'date_joined']
    list_display_links = ('first_name', 'last_name', 'email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    readonly_fields = ('last_login', 'date_joined',)
    ordering = ('-date_joined',)

admin.site.register(Account, AccountAdmin)
