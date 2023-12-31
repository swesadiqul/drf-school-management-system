# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated
# from drf_spectacular.utils import extend_schema
# from ..permission import IsSuperUser
# from ..models import Business, Type, UniversalEntities
# from ..serializers.universal_entity import TypeSerializer, UniversalEntitiesSerializer


# @extend_schema(
#     request=TypeSerializer,
#     responses={200: TypeSerializer(many=True)},
#     description='API endpoint to list and create types associated with a specific business. '
#                 'The API requires the user to be authenticated as a superuser.'
# )
# class TypeListCreateAPIView(APIView):
#     """
#     API endpoint to list and create types associated with a specific business.
#     """
#     permission_classes = [IsAuthenticated, IsSuperUser]

#     def get(self, request, business_id, *args, **kwargs):
#         # Get the business
#         business = get_object_or_404(Business, id=business_id)

#         # Get all types associated with the business
#         types = Type.objects.filter(business=business)
#         serializer = TypeSerializer(types, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, business_id, *args, **kwargs):
#         # Get the business
#         business = get_object_or_404(Business, id=business_id)

#         # Check if the user has permission to create types for this business
#         if not request.user.is_superuser:
#             return Response({'message': 'You do not have permission to create types for this business.'}, status=status.HTTP_403_FORBIDDEN)

#         serializer = TypeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(business=business)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @extend_schema(
#     request=None,
#     responses={
#         200: TypeSerializer,
#         400: 'Error: Bad Request',
#         403: 'Error: Forbidden',
#         404: 'Error: Not Found',
#         204: 'No Content'
#     },
#     description='API endpoint to retrieve, update, or delete a specific type associated with a business. '
#                 'The API requires the user to be authenticated as a superuser.'
# )
# class TypeDetailAPIView(APIView):
#     """
#     API endpoint to retrieve, update, or delete a specific type associated with a business.
#     """
#     permission_classes = [IsAuthenticated, IsSuperUser]

#     def get_object(self, business_id, type_id):
#         # Get the business
#         business = get_object_or_404(Business, id=business_id)

#         # Get the type associated with the business
#         return get_object_or_404(Type, id=type_id, business=business)

#     def get(self, request, business_id, type_id, *args, **kwargs):
#         type_instance = self.get_object(business_id, type_id)
#         serializer = TypeSerializer(type_instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, business_id, type_id, *args, **kwargs):
#         type_instance = self.get_object(business_id, type_id)
        
#         # Check if the user has permission to update this type
#         if not request.user.is_superuser:
#             return Response({'message': 'You do not have permission to update this type.'}, status=status.HTTP_403_FORBIDDEN)

#         serializer = TypeSerializer(type_instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, business_id, type_id, *args, **kwargs):
#         type_instance = self.get_object(business_id, type_id)
        
#         # Check if the user has permission to delete this type
#         if not request.user.is_superuser(type_instance):
#             return Response({'message': 'You do not have permission to delete this type.'}, status=status.HTTP_403_FORBIDDEN)

#         type_instance.delete()
#         return Response({'message': 'Type deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    
# @extend_schema(
#     request=None,
#     responses={
#         200: UniversalEntitiesSerializer(many=True),
#         201: UniversalEntitiesSerializer,
#         400: 'Error: Bad Request'
#     },
#     description='API endpoint to retrieve a list of universal entities or create a new universal entity. '
#                 'The API requires the user to be authenticated as a superuser.'
# )
# class UniversalEntitiesListCreateAPIView(APIView):
#     """
#     API endpoint to retrieve a list of universal entities or create a new universal entity.
#     """
#     permission_classes = [IsAuthenticated, IsSuperUser]
    
#     def get(self, request, *args, **kwargs):
#         # Get all universal entities
#         entities = UniversalEntities.objects.all()
#         serializer = UniversalEntitiesSerializer(entities, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         serializer = UniversalEntitiesSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# @extend_schema(
#     request=None,
#     responses={
#         200: UniversalEntitiesSerializer,
#         204: 'No Content',
#         400: 'Error: Bad Request'
#     },
#     description='API endpoint to retrieve, update, or delete a specific universal entity. '
#                 'The API requires the user to be authenticated as a superuser.'
# )
# class UniversalEntitiesDetailAPIView(APIView):
#     """
#     API endpoint to retrieve, update, or delete a specific universal entity.
#     """
#     permission_classes = [IsAuthenticated, IsSuperUser]
    
#     def get(self, request, universal_id, *args, **kwargs):
#         entity = get_object_or_404(UniversalEntities, pk=universal_id)
#         serializer = UniversalEntitiesSerializer(entity)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, universal_id, *args, **kwargs):
#         entity = get_object_or_404(UniversalEntities, pk=universal_id)
#         serializer = UniversalEntitiesSerializer(instance=entity, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, universal_id, *args, **kwargs):
#         entity = get_object_or_404(UniversalEntities, pk=universal_id)
#         entity.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
