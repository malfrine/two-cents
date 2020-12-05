from django.urls import path
from django.contrib import admin
from django.contrib.auth import logout

from django.conf.urls import include

from django.contrib.auth import views

from config.api import api



urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    
    path('api/', include(api.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
