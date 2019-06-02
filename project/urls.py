from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from .views import api_root


router = routers.DefaultRouter()

urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    re_path('api/(?P<version>(v1|v2))/', include('apps.scraped_suits.urls'))
]
