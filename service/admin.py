from django.contrib import admin

from service.models import Recipient, Message, Newsletter


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "name", "comment")
    list_filter = ("name",)
    search_fields = ("name", "email")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "body")
    list_filter = ("theme",)
    search_fields = ("theme",)
    list_editable = ("theme", "body")


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "end_time", "status", "message", "recipients")
    list_filter = ("status", "message")
    search_fields = ("status", "message")
    list_editable = ("start_time", "end_time")