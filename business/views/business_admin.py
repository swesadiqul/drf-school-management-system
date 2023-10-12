from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from ..permission import IsSuperUser, IsBusinessAdminUser
from ..models import Business
from ..serializers.business_admin import ListBusinessAdminSerializer, ListBusinessBranchAdminSerializer
from ..serializers.business import ListBusinessSerializer

CustomUser = get_user_model()

@extend_schema(
    request=None,
    responses={200: ListBusinessAdminSerializer(many=True)},
    description='API endpoint to list business administrators. '
                'The API requires the user to be authenticated as a superuser.'
)
class BusinessAdminListAPIView(APIView):
    """
    API endpoint to list business administrators.
    """
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, format=None):
        business_admin = CustomUser.objects.filter(is_business_admin=True)
        serializer = ListBusinessAdminSerializer(business_admin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    request=None, 
    responses={
        200: ListBusinessBranchAdminSerializer(many=True),
        404: 'Business not found or no branches available',
        403: 'Access denied: User is not a business admin or no permission'
    },
    description='API endpoint to retrieve the administrators of branches for a specific business. '
                'The API requires the user to be authenticated as a business admin.'
)
class BusinessBranchAdminAPIView(APIView):
    """
    API endpoint to list branch administrators for a specific business.
    """
    permission_classes = [IsAuthenticated, IsBusinessAdminUser]

    def get(self, request, business_id, *args, **kwargs):
        business = get_object_or_404(Business, id=business_id)

        # Check if the business has branches
        if not business.has_branch:
            return Response({'message': 'This business does not have any branches.'}, status=status.HTTP_200_OK)

        # Get the branches for the given business
        branches = Business.objects.filter(parent_business=business)

        # Get branch admins
        branches_admin = CustomUser.objects.filter(
            business__in=branches, is_branch_admin=True)

        # Serialize the data
        serialized_data = ListBusinessBranchAdminSerializer(
            branches_admin, many=True).data

        return Response({'branches_admin': serialized_data}, status=status.HTTP_200_OK)
