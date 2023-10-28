from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from django.utils import timezone
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from ..serializers.fees import FeesGroupSerializer, FeesTypeSerializer, FeesDiscountSerializer, FeesMasterSerializer, PaymentDetailsSerializer, FeesDueMessageSentSerializer
from ..models.fees import FeesGroup, FeesType, FeesMaster, FeesDiscount, FeesCollect, Payment
from ..models.student import Student
from ..tasks import send_email_to_student


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


class FeesDueMessageSentViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def fees_due_message_sent_students(self, request):
        class_id = request.data.get('class_id', None)
        section_id = request.data.get('section_id', None)
        last_date = request.data.get('last_date', None)
        common_message = request.data.get('common_message', None)

        if not last_date:
            return Response({"error": "Please specify 'last_date' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        if class_id and section_id:
            queryset = Student.objects.filter(
                current_class=class_id, current_section=section_id)
        elif class_id:
            queryset = Student.objects.filter(current_class=class_id)
        else:
            return Response({"error": "Please specify 'class_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        payments = Payment.objects.filter(
            fees_master__due_date__lt=last_date, status__in=['Unpaid', 'Partial'])

        # Use Prefetch to optimize the query and fetch related payments
        students = queryset.prefetch_related(
            Prefetch('fees_payments', queryset=payments, to_attr='filtered_payments'))

        serialized_data = []
        for student in students:
            if not student.reminder_sent:
                payments_data = []
                for payment in student.filtered_payments:
                    payments_data.append({
                        "payment_id": payment.payment_id,
                        "amount": payment.amount,
                        "status": payment.status,
                        "due_date": payment.fees_master.due_date
                    })

                # Prepare the message for the student
                if common_message:
                    message = common_message  # Use the common message
                else:
                    # If you want a unique message for each student, modify this part accordingly
                    message = f"Dear {student.user.get_full_name()}, you have dues to be paid."

                # Call the task asynchronously
                send_email_to_student.apply_async(
                    args=[student.user.email, "Dues Reminder", message])

                # Update the reminder_sent field
                student.reminder_sent = True
                student.save()

                student_data = {
                    "class_name": student.current_class.class_name if student.current_class else None,
                    "section_name": student.current_section.section_name if student.current_section else None,
                    "student_name": student.user.get_full_name() if student.user else None,
                    "student_email": student.user.email if student.user else None,
                    "payments": payments_data,
                    "message": message if message else None
                }
                serialized_data.append(student_data)

        return Response(serialized_data, status=status.HTTP_200_OK)


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


class PaymentDetailsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def get_payment_details(self, request):
        payment_id = request.data.get('payment_id', None)

        if payment_id:
            try:
                payment = FeesCollect.objects.get(payment_id=payment_id)
            except FeesCollect.DoesNotExist:
                return Response({"error": "Payment not found."}, status=status.HTTP_404_NOT_FOUND)

            serializer = PaymentDetailsSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Please specify 'payment_id' parameter."}, status=status.HTTP_400_BAD_REQUEST)
