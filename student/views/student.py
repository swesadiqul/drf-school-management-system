from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from usermanager.models import CustomUser
from student.models import Student
from student.serializers.student import StudentSerializer

class StudentListCreateView(APIView):

    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        student_serializer = StudentSerializer(data=request.data)

        try:
            if student_serializer.is_valid():
                student = student_serializer.save()
                return Response(student_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

