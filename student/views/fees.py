from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..serializers.fees import FeesGroupSerializer, FeesTypeSerializer, FeesDiscountSerializer, FeesMasterSerializer
from ..models.fees import FeesGroup, FeesType, FeesMaster, FeesDiscount


@extend_schema(
    request=FeesGroupSerializer,
    methods=['GET', 'POST'],
    description='API endpoint to list all fees groups or create a new fees group. '
                'The request for creating a fees group should contain details of the fees group to be created. '
                'This includes information such as group name and description. '
                'The API requires the user to be authenticated.'
)
class FeesGroupListCreateView(viewsets.ViewSet):
    """
    API endpoint to list all fees groups or create a new fees group.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def fees_group_list(self, request):
        """
        Get a list of all fees groups.
        """
        groups = FeesGroup.objects.all()
        serializer = FeesGroupSerializer(groups, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_fee_group(self, request):
        """
        Create a fees group.
        """
        serializer = FeesGroupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Fees group created successfully."}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
 

@extend_schema(
    request=FeesTypeSerializer,
    methods=['GET', 'POST'],
    description='API endpoint to list all fees types or create a new fees type. '
                'The request for creating a fees type should contain details of the fees type to be created. '
                'This includes information such as type name, fee code, and description. '
                'The API requires the user to be authenticated.'
)
class FeesTypeListCreateView(viewsets.ViewSet):
    """
    API endpoint to list all fees types or create a new fees type.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def fees_type_list(self, request):
        """
        Get a list of all fees types.
        """
        types = FeesType.objects.all()
        serializer = FeesTypeSerializer(types, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_fee_type(self, request):
        """
        Create a fees type.
        """
        serializer = FeesTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Fees type created successfully."}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

@extend_schema(
    request=FeesDiscountSerializer,
    methods=['GET', 'POST'],
    description='API endpoint to list all fees discounts or create a new fees discount. '
                'The request for creating a fees discount should contain details of the fees discount to be created. '
                'This includes information such as discount name, discount code, discount type, discount amount, discount percentage, and description. '
                'The API requires the user to be authenticated.'
)
class FeesDiscountListCreateView(viewsets.ViewSet):
    """
    API endpoint to list all fees discounts or create a new fees discount.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def fees_discount_list(self, request):
        """
        Get a list of all fees discounts.
        """
        discounts = FeesDiscount.objects.all()
        serializer = FeesDiscountSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_fee_discount(self, request):
        """
        Create a fees discount.
        """
        serializer = FeesDiscountSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Fees discount created successfully."}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    

@extend_schema(
    request=FeesMasterSerializer,
    methods=['GET', 'POST'],
    description='API endpoint to list all fees discounts or create a new fees discount. '
                'The request for creating a fees discount should contain details of the fees discount to be created. '
                'This includes information such as discount name, discount code, discount type, discount amount, discount percentage, and description. '
                'The API requires the user to be authenticated.'
)
class FeesMasterListCreateView(viewsets.ViewSet):
    """
    API endpoint to list all fees discounts or create a new fees discount.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def fees_master_list(self, request):
        """
        Get a list of all fees discounts.
        """
        discounts = FeesMaster.objects.all()
        serializer = FeesMasterSerializer(discounts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_fee_master(self, request):
        """
        Create a fees discount.
        """
        serializer = FeesMasterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Fees discount created successfully."}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)