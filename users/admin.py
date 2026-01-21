from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "full_name",
        "is_verified",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_verified", "is_active", "is_staff")
    search_fields = ("email", "username", "full_name")
    ordering = ("-created_at",)
