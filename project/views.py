from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'list-suits': reverse('list-suits', request=request, args=['v1'], format=format),
    })
