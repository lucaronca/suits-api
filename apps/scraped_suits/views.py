from rest_framework import generics
from .models import Suit
from .serializers import SuitSerializer


class ListSuitsView(generics.ListAPIView):
    """
    Provides a get method handler.
    """
    queryset = Suit.objects.all()
    serializer_class = SuitSerializer