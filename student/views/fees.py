from rest_framework.response import Response
from rest_framework.decorators import action
from decimal import Decimal
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models import F
from rest_framework import viewsets
from rest_framework import status
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from ..serializers.fees import FeesGroupSerializer, FeesTypeSerializer, FeesDiscountSerializer, FeesMasterSerializer, FeesCollectSerializer
from ..models.fees import FeesGroup, FeesType, FeesMaster, FeesDiscount, FeesCollect, Payment
from ..models.student import Class, Student
from ..serializers.fees import StudentSerializer


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
            # Calculate the due date (5 minutes from now in Asia/Dhaka timezone)
            current_time = timezone.now()
            due_date = current_time + timezone.timedelta(minutes=5)
            serializer.save(due_date=due_date)

            return Response({"message": "Fees discount created successfully."}, status=status.HTTP_201_CREATED)

        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class FeesTypeClassSearchView(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def search_fees_students(self, request):
        fees_type_ids = request.data.get('fees_type_ids', [])
        class_id = request.data.get('class_id', None)

        if not fees_type_ids or not class_id:
            return Response({'error': 'Please provide fees_type_ids and class_id.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({'error': 'Class does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        students = Student.get_students_by_class_id(class_id)

        if students is None:
            return Response({'error': 'No students found for the given class.'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare the response data
        response_data = []

        for student in students:
            student_info = {
                'class_name': selected_class.class_name,
                'student_email': student.user.email,
                'fees_groups': []  # List of fees groups for this student
            }

            total_amount = Decimal('0.00')

            for fees_type_id in fees_type_ids:
                try:
                    fees_master = FeesMaster.objects.get(id=fees_type_id)
                except FeesMaster.DoesNotExist:
                    response_data.append(
                        {'fees_type_id': fees_type_id, 'error': 'FeesMaster does not exist'})
                    continue

                # Fetch the student's fees_payments related to the fees_master
                student_fees_payments = student.fees_payments.filter(
                    id=fees_type_id)

                if student_fees_payments:
                    # Sum up the amounts for this fees_type_id for this student
                    fees_group_str = f"{fees_master.fees_group.group_name} - {fees_master.fees_type.type_name} ({fees_master.fees_type.fee_code})"
                    student_info['fees_groups'].append(fees_group_str)
                    total_amount += student_fees_payments.aggregate(
                        Sum('amount'))['amount__sum'] or Decimal('0.00')

            student_info['total_amount'] = str(total_amount)
            response_data.append({'student_info': student_info})

        return Response({'students': response_data}, status=status.HTTP_200_OK)

# class FeesTypeClassSearchView(viewsets.ViewSet):

    # @action(detail=False, methods=['get'])
    # def search_fees_students(self, request):
    #     fees_type_id = request.data['fees_type_id']
    #     class_id = request.data['class_id']

    #     if not fees_type_id or not class_id:
    #         return Response({'error': 'Please provide fees_type_id and class_id.'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         fees_master = FeesMaster.objects.get(id=fees_type_id)
    #     except FeesMaster.DoesNotExist:
    #         return Response({'error': 'FeesMaster does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         selected_class = Class.objects.get(id=class_id)
    #     except Class.DoesNotExist:
    #         return Response({'error': 'Class does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

    #     students = Student.get_students_by_class_id(class_id)

    #     if students is None:
    #         return Response({'error': 'No students found for the given class.'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Prepare the response data
    #     response_data = []
    #     for student in students:
    #         student_info = {
    #             'class_name': selected_class.class_name,
    #             # 'student_name': student.user.get_full_name(),
    #             'fees_group': fees_master.fees_group.group_name,
    #             'amount': fees_master.amount
    #         }

    #         # Fetch the student's fees_payments related to the fees_master
    #         student_fees_payments = student.fees_payments.filter(id=fees_type_id)

    #         print(student_fees_payments)
    #         if student_fees_payments:
    #             student_info['fees_payments'] = list(student_fees_payments.values('due_date', 'amount'))
    #         else:
    #             student_info['fees_payments'] = []

    #         response_data.append(student_info)

    #     return Response({'students': response_data}, status=status.HTTP_200_OK)


class FeesCollectViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def collect_fees(self, request, student_id=None):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({'error': f'Student with ID {student_id} not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get all payments related to the student with unpaid status
        payments = student.fees_payments.filter(
            status__in=['Unpaid', 'Partial'])

        payments_data = request.data['payments']

        for payment_data in payments_data:
            pay_id = payment_data.get('pay_id')
            amount_collected = payment_data.get('collect')['amount']
            payment_mode = payment_data.get('collect')['payment_mode']
            discount_group = payment_data.get('collect').get('discount', None)

            try:
                payment = payments.get(pay_id=pay_id)
            except Payment.DoesNotExist:
                return Response({'error': f'Payment with pay_id {pay_id} not found.'}, status=status.HTTP_400_BAD_REQUEST)

            if amount_collected > payment.amount:
                return Response({'error': f'Amount collected cannot be greater than the amount due.'}, status=status.HTTP_400_BAD_REQUEST)
            elif amount_collected == 0:
                return Response({'error': f'Amount collected cannot be zero.'}, status=status.HTTP_400_BAD_REQUEST)

             # Handle the discount based on the discount group
            if discount_group is not None:
                try:
                    fees_discount = FeesDiscount.objects.get(pk=discount_group)
                    if fees_discount.discount_type == 'Fixed':
                        # Apply a fixed discount
                        amount_collected += fees_discount.discount_amount
                    elif fees_discount.discount_type == 'Percentage':
                        # Apply a percentage discount
                        percentage_discount = (
                            fees_discount.discount_percentage / 100) * amount_collected
                        amount_collected += percentage_discount
                    else:
                        return Response({'error': 'Invalid discount type specified.'}, status=status.HTTP_400_BAD_REQUEST)
                except FeesDiscount.DoesNotExist:
                    return Response({'error': f'Discount group {discount_group} not found.'}, status=status.HTTP_400_BAD_REQUEST)

            print(amount_collected)
            if (payment.paid + amount_collected) > payment.amount:
                return Response({'error': f'Amount collected cannot be greater than the amount due.'}, status=status.HTTP_400_BAD_REQUEST)

            # Update payment details
            if amount_collected == payment.amount or (payment.amount == (payment.paid + amount_collected)):
                payment.paid = payment.paid + amount_collected
                payment.balance = 0
                payment.status = 'Paid'
            else:
                payment.paid = payment.paid + amount_collected
                payment.balance = payment.amount - payment.paid
                payment.status = 'Partial'

            # Increment the paid amount and update the balance
            payment.save()

            # Generate unique payment_id for each payment if it's blank
            if not payment.payment_id:
                existing_payment_ids = Payment.objects.filter(payment_id__startswith=f"{pay_id:03}").values_list(
                    'payment_id', flat=True)
                count = existing_payment_ids.count()

                unique_payment_id = f"{pay_id:03}"
                payment.payment_id = unique_payment_id
                payment.save()

            # Create a FeesCollect record for this payment

            existing_records = FeesCollect.objects.filter(
                payment_id__startswith=payment.payment_id)
            count = existing_records.count() + 1
            print(existing_records, count)
            fees_collect = FeesCollect.objects.create(
                amount=amount_collected,
                payment_mode=payment_mode,
                payment_id=f"{payment.payment_id}/{count}",
                note=f'Payment collected for Payment ID: {payment.payment_id}/{count}'
            )

        return Response({'message': 'Fees collected successfully.'}, status=status.HTTP_200_OK)
