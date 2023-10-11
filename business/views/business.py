from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from ..permission import IsSuperUser, IsBusinessAdminUser, IsBranchPermission
from ..models import Business, Type, UniversalEntities
from ..serializers.business import CreateBusinessSerializer, ListBusinessSerializer, CreateBusinessBranchSerializer, BusinessBranchesListSerializer


CustomUser = get_user_model()


class CreateBusinessAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = CreateBusinessSerializer(data=request.data)
        try:
            if serializer.is_valid():
                business = serializer.save()
                return Response(CreateBusinessSerializer(business).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BusinessListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get(self, request, format=None):
        businesses = Business.objects.all()
        serializer = ListBusinessSerializer(businesses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateBusinessBranchAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsBusinessAdminUser, IsBranchPermission]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Check the branch creation limit
        if user.branch_limit <= 0:
            return Response({'message': 'You have reached the limit for branch creation.'}, status=status.HTTP_403_FORBIDDEN)

        # Decrement the branch creation limit
        user.branch_limit -= 1
        user.save()

        # Get parent business for the branch
        parent_business_id = request.data.get('parent_business_id')
        parent_business = get_object_or_404(Business, id=parent_business_id)

        # Remove unwanted fields for branch
        request.data.pop('has_branch', None)
        request.data.pop('branch_num', None)

        serializer = CreateBusinessBranchSerializer(data=request.data)
        if serializer.is_valid():
            # Create the branch
            serializer.save(parent_business=parent_business)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessBranchesListView(APIView):
    
    permission_classes = [IsAuthenticated, IsBusinessAdminUser]
    
    def get(self, request, business_id, *args, **kwargs):
        business = get_object_or_404(Business, id=business_id)
        branches = Business.objects.filter(parent_business=business)

        serializer = ListBusinessSerializer(business)
        data = {
            'business': serializer.data,
            'has_branches': branches.exists(),
            'branches': BusinessBranchesListSerializer(branches, many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)
    


    
