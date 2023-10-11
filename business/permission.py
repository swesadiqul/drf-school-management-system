from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True
        else:
            return Response({'message': 'You are not authorized super user.'}, status=status.HTTP_403_FORBIDDEN)


class IsBusinessAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_business_admin:
            return True
        else:
            return Response({'message': 'You are not authorized business admin.'}, status=status.HTTP_403_FORBIDDEN)


class IsBranchPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_business_admin and request.user.is_create_branch:
            return True
        return Response({'message': 'You are not authorized to create a branch.'}, status=status.HTTP_403_FORBIDDEN)
