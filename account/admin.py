from django.contrib import admin
from .models import UserAccount
# Register your models here.
class UserAccountModelAdmin(admin.ModelAdmin):
    list_display = ['user','account_no','balance', 'image']

admin.site.register(UserAccount,UserAccountModelAdmin)