from django.contrib import admin
from .models import Fleek, FleeksLike, FleeksImage


class FleeksLikeAdmin(admin.TabularInline):
    model = FleeksLike

class FleekAdmin(admin.ModelAdmin):
    inlines = [FleeksLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__user__username', 'user__user__email']
    class Meta:
        model = Fleek

admin.site.register(Fleek, FleekAdmin)

admin.site.register(FleeksImage)