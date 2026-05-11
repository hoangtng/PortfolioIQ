from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("PortfolioIQ", {"fields": ("telegram_chat_id",)}),
    )
    readonly_fields = BaseUserAdmin.readonly_fields + ("created_at",)
    
    list_display = ("username", "email", "telegram_chat_id", "is_staff", "created_at")