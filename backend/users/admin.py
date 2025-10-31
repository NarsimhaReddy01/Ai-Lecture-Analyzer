from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {"fields": ("role",)}),
    )
    list_display = UserAdmin.list_display + ("role",)

admin.site.register(User, CustomUserAdmin)
