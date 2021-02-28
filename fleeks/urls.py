
from django.urls import path
from .views import (
    fleeks_list_view,
    fleeks_feed_view,
    fleek_action_view,
    fleek_delete_view,
    fleek_detail_view,
    GetFleekDetail,
    fleek_create_view,
    FleekCreateView,
)


app_name = 'fleeks'





fleekcreateview = FleekCreateView.as_view({'post':'create'})


urlpatterns = [
    path('creates/', fleekcreateview, name="fleekscreate"),
    path('', fleeks_list_view),
    path('feed/', fleeks_feed_view),
    path('action/', fleek_action_view),
    path('create/', fleek_create_view),
    path('<int:fleek_id>/', fleek_detail_view),
    path('get/<int:id>/', GetFleekDetail, name='fleek_detail'),
    path('<int:fleek_id>/delete/', fleek_delete_view),
]