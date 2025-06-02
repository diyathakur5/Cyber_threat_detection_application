from django.contrib import admin
from .models import SpamMessage, SpamURL, SpamPhoneNumber

@admin.register(SpamMessage)
class SpamMessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'is_spam', 'reported_at')
    search_fields = ('content',)

@admin.register(SpamURL)
class SpamURLAdmin(admin.ModelAdmin):
    list_display = ('url', 'is_spam', 'reported_at')
    search_fields = ('url',)

@admin.register(SpamPhoneNumber)
class SpamPhoneNumberAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'is_spam', 'reported_at')
    search_fields = ('phone_number',)
