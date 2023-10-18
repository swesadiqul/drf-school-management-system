from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.parent import  Parent
from ..serializers.parent import ParentSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    request=ParentSerializer,
    methods=['GET'],
    description='API endpoint to list all parents.'
                'The request to show all listed parents in database.'
                'The API requires the user to be authenticated.'
)
class ParentListView(APIView):
    """
    API endpoint to list all parents.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        parents = Parent.objects.all()
        serializer = ParentSerializer(parents, many=True)
        return Response(serializer.data)
    
