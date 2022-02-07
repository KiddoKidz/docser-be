from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models


class CustomUserAdmin(UserAdmin):
    model = models.CustomUser
    list_display = ("email", "is_admin", "is_active")
    list_filter = ("email",)
    fieldsets = (
        (
            "Data",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                )
            },
        ),
        ("Permissions", {"fields": ("is_admin", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    filterset_fields = ("email",)
    ordering = ("email",)


# Register your models here.
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.UserOAuth2Credentials)
