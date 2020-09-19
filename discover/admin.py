from django.contrib import admin

from .models import Category, Product, ViewsNumber, PaymentMethod, PurchaseOrder, PurchaseItem, PurchasePaymentMethod, Post, ProductImage
    


admin_models = [
    Post, ProductImage, Category, Product, PaymentMethod, PurchaseOrder,
    PurchaseItem, PurchasePaymentMethod, ViewsNumber,
]


for item in admin_models:
    admin.site.register(item)