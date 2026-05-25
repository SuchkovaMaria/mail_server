from django.contrib import admin
from django.contrib.auth.models import Permission
from users.models import User


@admin.register(User)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "phone", "token", 'get_groups', "block_status")
    list_filter = ("email",)
    search_fields = ("phone", "email")

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

        get_groups.short_description = "Groups"

@admin.register(Permission)
class PermitionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename")

