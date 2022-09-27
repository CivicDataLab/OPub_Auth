from django.contrib import admin

# Register your models here.

from .models import CustomUser, Permissions
from graphql_auth.models import UserStatus

admin.site.register(UserStatus)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username","email"]
    # readonly_fields = ('created_on','updated_on') 

    class Meta:
        model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Permissions)