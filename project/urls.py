from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    re_path('api/(?P<version>(v1|v2))/', include('apps.scraped_suits.urls'))
]
