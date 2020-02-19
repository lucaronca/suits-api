from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework.renderers import JSONRenderer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'list-suits': reverse('list-suits', request=request, args=['v1'], format=format),
    })


class StatusCheckView(generics.GenericAPIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        return Response({
            'status': 'ok'
        })
