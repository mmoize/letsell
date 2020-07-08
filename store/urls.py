from django.urls import path

from .views import (
    CategoryCreateView,
    ProductCreateView,
    PaymentMethodCreateView,
    PurchaseOrderCreateView,
    PurchaseItemCreateView
)


app_name = 'store'

urlpatterns = [
    path(
        'categories/',
        CategoryCreateView.as_view(),
        name='categories'
    ),
    path(
        'products/',
        ProductCreateView.as_view(),
        name='products'
    ),
    path(
        'payment-methods/',
        PaymentMethodCreateView.as_view(),
        name='payment-methods'
    ),
    path(
        'purchase-orders/',
        PurchaseOrderCreateView.as_view(),
        name='purchase-orders'
    ),
    path(
        'purchase-items/',
        PurchaseItemCreateView.as_view(),
        name='purchase-items'
    ),
]