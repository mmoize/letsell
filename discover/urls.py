from django.urls import path

from discover.views import (
    CategoryCreateView,
    ProductCreateView,
    PaymentMethodCreateView,
    PurchaseOrderCreateView,
    PurchaseItemCreateView,
    CategoryView,
    Product_list,
    PostCreatView,
    PostView,
    ProfileUserListings,
    Product_image_list,
    PostDetailView,
    Post_DetailView,
    ProductImageViewSet,
    ProductImageset,
    PostsAndroidAPI,
    UserProductView,
    UserDeleteProductView,
    UserPostView,
    UserDeletePostView,
    Postfilterview,
    SearchPost,
    PostSearchView,
    PostLocation,
    PostViaLocationView,
    ProfileUserPostsAndroidAPI,
    UserPostsAndroidAPI
)
  

view_categories = CategoryView.as_view({'get': 'list'})
#------------------------end-categories
postcreateview = PostCreatView.as_view({'post': 'create'})
postview = PostCreatView.as_view({'get': 'list'})
postdetailview = PostDetailView.as_view({'get': 'list'})
postSearchview = PostSearchView.as_view({'get': 'list'})
postlocation = PostLocation.as_view({'get': 'list'})
postviewvialocation=PostViaLocationView.as_view({'get': 'list'})


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
   
    path('userdeleteproductview/<int:pk>', UserDeleteProductView.as_view(), name='delete_product_view-detail'),
    path('userproductview/', UserProductView.as_view({'get': 'list'}), name='productview-detail'),
    path('viewproduct/', Product_list, name='products-detail'),
    path('viewproductimage/', ProductImageViewSet.as_view({'get': 'list'}), name='productimage-detail'),
    path('imageset/<int:id>/', ProductImageset.as_view(), name='imageset-detail'),
    path('postsandroidapi/', PostsAndroidAPI.as_view(), name='posts_android_api'),
    path('profileuserpostsandroidapi/', ProfileUserPostsAndroidAPI.as_view(), name='profile_user_posts_android_api'),
    path('userpostsandroidapi/<int:id>/', UserPostsAndroidAPI.as_view(), name='user_posts_android_api'),
    #------------------------end-products
    path('viewpostfilter/<int:category>', Postfilterview.as_view(), name='post_category_filter-detail'),
    path('viewpostsearch/', SearchPost.as_view(), name='post_category_filter-detail'),
     path('postviewvialocation/', postviewvialocation, name='post_view_via_location-detail'),
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
    path('userdeletepostview/<int:pk>', UserDeletePostView.as_view(), name='delete_post_view-detail'),
    path('postviewer/', PostView),
    path('userpostview/', UserPostView.as_view({'get': 'list'}), name='userpostview-detail'),
    
    path('getprofilepostlisting/<int:id>' , ProfileUserListings, name='products'),
    path('postdetail/<int:id>', postdetailview , name='postdetail'),
    path('postsearchview/', postSearchview , name='postsearch'),
    path('postlocationview/', postlocation , name='postlocation'),

    path(
        'postdetails/',
        Post_DetailView.as_view(),
        name='productview'
    ),
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