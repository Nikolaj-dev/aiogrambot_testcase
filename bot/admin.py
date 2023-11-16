from django.contrib import admin
from .models import TelegramChat, CurrencyHistory


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'user')
    search_fields = ('chat_id', 'user__username')  # Добавьте поля, по которым вы хотите выполнять поиск


@admin.register(CurrencyHistory)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'code', 'name', 'rate', 'date', 'inverseRate', 'user')
    search_fields = ('code', 'name', 'date', 'user__username')  # Добавьте поля, по которым вы хотите выполнять поиск

