from django.urls import path

from discover.views import (
    CategoryCreateView,
    ProductCreateView,
    PaymentMethodCreateView,
    PurchaseOrderCreateView,
    PurchaseItemCreateView,
    CategoryView,
    ProductsView,
    Product_list,
    PostCreatView,
    PostView,
    Post_list,
    Product_image_list
)
  

view_categories = CategoryView.as_view({'get': 'list'})
#------------------------end-categories
postcreateview = PostCreatView.as_view({'post': 'create'})
postview = PostCreatView.as_view({'get': 'list'})


app_name = 'discover'

urlpatterns = [
    path(
        'categories/',
        CategoryCreateView.as_view(),
        name='categories'
    ),
    path(
        'view_categories/',
        view_categories,
        name='view_categories'
    ),
    #------------------------end-categories
    path(
        'products/',
        ProductCreateView.as_view({'post': 'create'}),
        name='products'
    ),
    path(
        'productview/',
        ProductsView.as_view(),
        name='productview'
    ),
    path('viewproduct/', Product_list, name='products'),
     path('viewproductimage/', Product_image_list, name='productimage-detail'),
    #------------------------end-products


    #------------------------end-products
    path(
        'postcreateview/<int:id>',
        postcreateview,
        name='post_create'
    ),
    path(
        'postview/',
        postview,
        name='post_view'
    ),
    path('postviewer/', PostView),
    
     path('viewpost/', Post_list, name='products'),
    #------------------------end-post

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