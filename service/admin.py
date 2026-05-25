from django.contrib import admin

from service.models import Recipient, Message, Newsletter


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "comment", "owner", "owner_group")
    list_filter = ("name", "owner", "owner_group")
    search_fields = ("name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "body", "owner", "owner_group")
    list_filter = ("theme", "owner", "owner_group")
    search_fields = ("theme",)
    list_editable = ("theme", "body")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "message", "owner", "owner_group", "activity_status")
    list_filter = ("status", "message", "owner", "owner_group")
    search_fields = ("status",)
    search_fields = ("status", "message")
    list_editable = ("start_time", "end_time")