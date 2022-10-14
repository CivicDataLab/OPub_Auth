from django.contrib import admin

# Register your models here.

from .models import *
from graphql_auth.models import UserStatus

admin.site.register(UserStatus)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username","email"]
    # readonly_fields = ('created_on','updated_on') 

    class Meta:
        model = CustomUser
        
class RoleAdmin(admin.ModelAdmin):
    list_display = ["role_name","role_verbose_name"]
    # readonly_fields = ('created_on','updated_on') 

    class Meta:
        model = Role
        
class PermissionAdmin(admin.ModelAdmin):
    list_display = ["perm_name","perm_verbose_name"]
    # readonly_fields = ('created_on','updated_on') 

    class Meta:
        model = Permission
        
        
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ["role","permission"]
    # readonly_fields = ('created_on','updated_on') 

    class Meta:
        model = RolePermission
        
    
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["username","org_id", "role"]

    class Meta:
        model = UserRole
        
class DatsetOwnerAdmin(admin.ModelAdmin):
    list_display = ["username","dataset_id","is_owner"]
    # readonly_fields = ('created_on','updated_on') 

    class Meta:
        model = DatasetOwner

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RolePermission, RolePermissionAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(DatasetOwner, DatsetOwnerAdmin)