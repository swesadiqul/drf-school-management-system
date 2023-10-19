from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from ..models.student import Student, StudentAdmission, Section, Class, PromoteStudents
from ..serializers.student import StudentSerializer, StudentAdmissionSerializer, SectionSerializer, ClassSerializer, PromoteStudentSerializer, PromoteAllStudentsSerializer



@extend_schema(
    request=SectionSerializer,
    methods=['GET', 'POST'],
    responses={200: SectionSerializer(many=True)},
    description='API endpoint to list all section or create a new section. '
                'The request for creating a section should contain details of the student to be created. '
                'The API requires the user to be authenticated.'
)
class SectionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        sections = Section.objects.all()
        serializer = SectionSerializer(sections, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ClassSerializer,
    methods=['GET', 'POST'],
    responses={200: ClassSerializer(many=True)},
    description='API endpoint to list all class or create a new class. '
                'The request for creating a class should contain details of the class to be created. '
                'The API requires the user to be authenticated.'
)
class ClassListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=StudentAdmissionSerializer,
    methods=['GET', 'POST'],
    responses={200: StudentAdmissionSerializer(many=True)},
    description='API endpoint to list all student admissions or create a new student admission. '
                'The request for creating a student admission should contain details of the student to be created. '
                'This includes information such as user details, parent email, gender, country, etc. '
                'The API requires the user to be authenticated.'
)
class StudentAdmissionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        student_admissions = StudentAdmission.objects.all()
        serializer = StudentAdmissionSerializer(student_admissions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentAdmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=StudentSerializer,
    methods=['GET'],
    description='API endpoint to list all students. It will return three types of students: '
                '1. All students, 2. Disabled students, 3. Enabled students. '
                'This includes information such as user details, parent email, gender, country, etc. '
                'The API requires the user to be authenticated.'
)
class StudentListView(viewsets.ViewSet):
    """
    API endpoint to list all students.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_students(self, request):
        """
        List all students.
        """
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_disabled_students(self, request):
        """
        List all disabled students.
        """
        students = Student.objects.filter(is_disable=True)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def list_enabled_students(self, request):
        """
        List all enabled students.
        """
        students = Student.objects.filter(is_disable=False)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@extend_schema(
    request=PromoteStudentSerializer,
    methods=['POST'],
    description='API endpoint to promote a single student or all students in a class to the next desired    class. '
            'The request should contain the student ID, target class ID, target section ID, and optional remarks.'
            'The API requires the user to be authenticated.'
)
class PromoteStudentListCreateView(viewsets.ViewSet):
    """
    API endpoint to list all promoted students or promote a single student.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def promote_student(self, request):
        """
        Promote a single student to the next desired class.
        """
        serializer = PromoteStudentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                student_id = request.data['student_id']
                to_class_id = request.data['to_class_id']
                to_section_id = request.data['to_section_id']
                remarks = request.data.get('remarks', '')

                student = Student.objects.get(pk=student_id)
                to_class = Class.objects.get(pk=to_class_id)
                to_section = Section.objects.get(pk=to_section_id)

                promotion = PromoteStudents.objects.create(
                    student=student,
                    from_class=student.current_class,
                    to_class=to_class,
                    from_section=student.current_section,
                    to_section=to_section,
                    remarks=remarks
                )
                
                promotion.save()

                student.current_class = to_class
                student.current_section = to_section
                student.save()

                return Response({"message": "Student promoted successfully.", "promotion_id": promotion.promotion_id}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def promote_all_students(self, request):
        """
        Promote all students of a class to the next desired class.
        """
        serializer = PromoteAllStudentsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                from_class_id = request.data['from_class_id']
                to_class_id = request.data['to_class_id']
                to_section_id = request.data['to_section_id']
                remarks = request.data.get('remarks', '')

                from_class = Class.objects.get(pk=from_class_id)
                to_class = Class.objects.get(pk=to_class_id)
                to_section = Section.objects.get(pk=to_section_id)

                students_to_promote = Student.objects.filter(
                    current_class=from_class)

                for student in students_to_promote:
                    promotion = PromoteStudents.objects.create(
                        student=student,
                        from_class=from_class,
                        to_class=to_class,
                        from_section=student.current_section,
                        to_section=to_section,
                        remarks=remarks
                    )

                    student.current_class = to_class
                    student.current_section = to_section
                    student.save()

                return Response({"message": "Students promoted successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





