from django.contrib import admin
from .models import Member

class MessageAdmin(admin.ModelAdmin):
    model = Member
    list_display = ('user', 'id')


admin.site.register(Member, MessageAdmin)

