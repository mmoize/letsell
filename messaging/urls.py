from django.urls import path

from .views import MessageCreateView, MessageDetailView, MessagelistView, InboxView


app_name = 'messaging'
messagecreateview = MessageCreateView.as_view({'post': 'create'})
messagedetailview = MessageDetailView.as_view({'get': 'list'})
# messageListview = MessagelistView.as_view({'get'})

urlpatterns = [
    # path('messagelistview/', messageListview , name='message_list'),
    path('messagecreate/<str:username>/',messagecreateview , name='messagecreate'),
    path('messagedetailview/', MessagelistView.as_view({'get': 'list'}), name='message_detail'),
        path(
        'messages/',
        InboxView.as_view(),
        name='messages'
    ),
]

