"""letsell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls', namespace='authentication')),
    path('api/', include('accounts.urls', namespace='accounts')),
    path('api/core/', include('core.urls', namespace='core')),
    path('api/', include('discover.urls', namespace='discover')),
    path('api/fleeks/', include('fleeks.urls', namespace='fleeks')),
    path('api/fleeksvideo/', include('fleeksvideo.urls', namespace='fleeksvideo')),
    path('api/chat/', include('chat.urls', namespace='chat')),
    path('api/devices/', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    path('api/devicex/', GCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace="password_rest")), 
]
