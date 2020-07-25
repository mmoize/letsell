from django.contrib import admin
from .models import Message, Room

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('sender', 'recipient')


admin.site.register(Message, MessageAdmin)
admin.site.register(Room)
