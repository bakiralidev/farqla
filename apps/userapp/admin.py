from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # read-only qilib qo'yamiz — formga qo'yish mumkin, lekin tahrirlab bo'lmaydi
    readonly_fields = ("date_joined", "last_login")

    ordering = ("-date_joined",)
    list_display = ("id", "phone", "name", "email", "is_active", "is_staff")
    search_fields = ("phone", "email", "name")
    list_filter = ("is_active", "is_staff", "is_superuser", "groups")

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("name", "email")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),  # readonly_fields tufayli ok
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_active", "is_staff", "is_superuser", "groups"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")
