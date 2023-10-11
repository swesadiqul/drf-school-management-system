from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, reverse
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from ..permission import IsSuperUser, IsBusinessAdminUser
from ..models import Business
from ..serializers.business_admin import ListBusinessAdminSerializer, ListBusinessBranchAdminSerializer
from ..serializers.business import ListBusinessSerializer

CustomUser = get_user_model()


class BusinessAdminListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, format=None):
        business_admin = CustomUser.objects.filter(is_business_admin=True)
        serializer = ListBusinessAdminSerializer(business_admin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessBranchAdminAPIView(APIView):

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
