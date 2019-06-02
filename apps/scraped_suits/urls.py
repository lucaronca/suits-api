from django.urls import path
from .views import ListSuitsView


urlpatterns = [
    path('suits/', ListSuitsView.as_view(), name="list-suits")
]
