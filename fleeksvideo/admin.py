from django.contrib import admin


from .models import Fleek, FleekLike, Comment
    


admin_models = [
    Fleek, FleekLike, Comment
]


for item in admin_models:
    admin.site.register(item)