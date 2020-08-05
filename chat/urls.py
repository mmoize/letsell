from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import  PostMessage
from .views import RoomView, LobbyView,  MainView, PostMessagexist
from . import views





app_name = 'chat'

urlpatterns = [
    path('room/<int:id>', RoomView.as_view() ,name='room-detail'), 
    path('room/<int:id>/<int:page>', RoomView.as_view() ,name='room_page-detail'), 

    path('lobby/', LobbyView.as_view(), name="lobby-detail"), 
    path('main/',  MainView.as_view(), name='main-detail'), 
    path('postmessagex/', PostMessage.as_view({'post': 'create'}), name='message_post'),
    # posting message should include: (message, title, ref-post, recipient)
    path('postmessagex/<int:id>', PostMessage.as_view({'post': 'create'}), name='message_post'),
    path('postmessager/<int:id>', PostMessagexist.as_view({'post': 'create'}), name='message_post'),

]

