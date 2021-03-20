from django.contrib import admin
from .models import Fleeka, FleeksImage



class FleekAdmin(admin.ModelAdmin):
    #inlines = [FleeksLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__user__username', 'user__user__email']
    class Meta:
        model = Fleeka

admin.site.register(Fleeka, FleekAdmin)

admin.site.register(FleeksImage)