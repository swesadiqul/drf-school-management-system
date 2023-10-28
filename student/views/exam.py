from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from ..serializers.exam import ExamTypeSerializer, ExamGroupSerializer, ExamSerializer, MarksGradeSerializer, MarksDivisionSerializer, AdmitCardDesignSerializer, MarksheetDesignSerializer
from ..models.exam import ExamType, ExamGroup, Exam, MarksGrade, MarksDivision, AdmitCardDesign, MarksheetDesign
from ..models.student import Student


class ExamTypeViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_exam_types(self, request):
        queryset = ExamType.objects.all()
        serializer = ExamTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_exam_type(self, request):
        serializer = ExamTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExamViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_exams(self, request):
        queryset = Exam.objects.all()
        serializer = ExamSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_exam(self, request):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExamGroupViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_exam_groups(self, request):
        queryset = ExamGroup.objects.all()
        serializer = ExamGroupSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_exam_group(self, request):
        serializer = ExamGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ExamScheduleViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def group_exams_schedule(self, request):
        group_id = request.data.get('group_id', None)
        exam_id = request.data.get('exam_id', None)

        try:
            # Query the ExamGroup by its ID
            exam_group = ExamGroup.objects.get(id=group_id)
            exams = exam_group.exam.all()  # Access the related exams from the ExamGroup instance

            # Check if both group_id and exam_id are provided and exist in the group
            if group_id is not None and exam_id is not None:
                try:
                    exam = exams.get(id=exam_id)
                    serializer = ExamSerializer(exam)
                    data = serializer.data
                    data['subject_info'] = serializer.get_subject_info(
                        exam)  # Add subject information
                    return Response(data, status=status.HTTP_200_OK)
                except Exam.DoesNotExist:
                    return Response({"error": "Exam not found in the specified group"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ExamGroupSerializer(exam_group)
            data = serializer.data
            data['exams'] = ExamSerializer(exams, many=True).data
            for exam in data['exams']:
                exam['subject_info'] = serializer.get_subject_info(
                    exam)  # Add subject information to each exam
            return Response(data, status=status.HTTP_200_OK)

        except ExamGroup.DoesNotExist:
            return Response({"error": "ExamGroup not found"}, status=status.HTTP_404_NOT_FOUND)


class MarksGradeViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_marks_grades(self, request):
        marks_grades = MarksGrade.objects.all()
        serializer = MarksGradeSerializer(marks_grades, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=['post'])
    def create_marks_grade(self, request):
        serializer = MarksGradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'])
    def get_grades_by_exam_type(self, request):
        exam_type_id = request.data.get('exam_type_id')

        try:
            exam_type = ExamType.objects.get(id=exam_type_id)
        except ExamType.DoesNotExist:
            return Response({"error": "ExamType not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get all grades related to the specified exam_type
        grades = MarksGrade.objects.filter(exam_type=exam_type)

        # Serialize the grades
        grade_serializer = MarksGradeSerializer(grades, many=True)

        # Serialize the exam type
        exam_type_serializer = ExamTypeSerializer(exam_type)

        response_data = {
            "exam_type": exam_type_serializer.data,
            "grades": grade_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class MarksDivisionViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def list_marks_divisions(self, request):
        marks_divisions = MarksDivision.objects.all()
        serializer = MarksDivisionSerializer(marks_divisions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_marks_division(self, request):
        serializer = MarksDivisionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdmitCardDesignViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def get_admit_card(self, request):
        admit_card_id = request.data.get('admit_card_id')

        try:
            admit_card = AdmitCardDesign.objects.get(id=admit_card_id)
            serializer = AdmitCardDesignSerializer(admit_card)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AdmitCardDesign.DoesNotExist:
            return Response({"error": "Admit Card not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def generate_admit_card(self, request):
        template_name = request.data.get('template_name')
        heading = request.data.get('heading')
        title = request.data.get('title')
        exam_id = request.data.get('exam_id')
        school_name = request.data.get('school_name')
        exam_center = request.data.get('exam_center')
        footer_text = request.data.get('footer_text')
        left_logo = request.FILES['left_logo']
        right_logo = request.FILES['right_logo']
        sign = request.FILES['sign']
        background_image = request.FILES['background_image']
        student_id = request.data.get('student_id')

        try:
            exam = Exam.objects.get(id=exam_id)
            student = Student.objects.get(id=student_id)

            admit_card_design = AdmitCardDesign.objects.create(
                template_name=template_name,
                heading=heading,
                title=title,
                exam=exam,
                school_name=school_name,
                exam_center=exam_center,
                footer_text=footer_text,
                left_logo=left_logo,
                right_logo=right_logo,
                sign=sign,
                background_image=background_image,
                student=student
            )

            serializer = AdmitCardDesignSerializer(admit_card_design)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


class MarksheetDesignViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_marksheet_design(self, request):
        marksheet_design_id = request.data.get('marksheet_design_id')

        try:
            marksheet_design = MarksheetDesign.objects.get(id=marksheet_design_id)
            serializer = MarksheetDesignSerializer(marksheet_design)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MarksheetDesign.DoesNotExist:
            return Response({"error": "Marksheet Design not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def generate_marksheet_design(self, request):
        template_name = request.data.get('template_name')
        heading = request.data.get('heading')
        title = request.data.get('title')
        exam_id = request.data.get('exam_id')
        school_name = request.data.get('school_name')
        exam_center = request.data.get('exam_center')
        footer_text = request.data.get('footer_text')
        body_text = request.data.get('body_text')
        header_image = request.FILES['header_image']
        left_logo = request.FILES['left_logo']
        right_logo = request.FILES['right_logo']
        left_sign = request.FILES['left_sign']
        middle_sign = request.FILES['middle_sign']
        right_sign = request.FILES['right_sign']
        background_image = request.FILES['background_image']
        student_id = request.data.get('student_id')
        

        try:
            exam = Exam.objects.get(id=exam_id)
            student = Student.objects.get(id=student_id)

            marksheet_design = MarksheetDesign.objects.create(
                template_name=template_name,
                heading=heading,
                title=title,
                exam=exam,
                school_name=school_name,
                exam_center=exam_center,
                footer_text=footer_text,
                body_text=body_text,
                header_image=header_image,
                left_logo=left_logo,
                right_logo=right_logo,
                left_sign=left_sign,
                middle_sign=middle_sign,
                right_sign=right_sign,
                background_image=background_image,
                student=student
            )

            serializer = MarksheetDesignSerializer(marksheet_design)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exam.DoesNotExist:
            return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


class StudentAdmitCardSearchView(viewsets.ViewSet):
    serializer_class = AdmitCardDesignSerializer

    @action(detail=False, methods=['post'])
    def search_admit_card(self, request):
        group_id = request.data.get('group_id')
        exam_id = request.data.get('exam_id')
        class_id = request.data.get('class_id')
        student_id = request.data.get('student_id')

        try:
            # Query the ExamGroup by its ID
            exam_group = ExamGroup.objects.get(id=group_id)
            exams = exam_group.exam.all()  # Access the related exams from the ExamGroup instance

            # Check if both group_id and exam_id are provided and exist in the group
            if group_id is not None and exam_id is not None:
                try:
                    exam = exams.get(id=exam_id)

                    # Check if the specified student is in the specified class
                    student = Student.objects.filter(
                        id=student_id, current_class_id=class_id).first()

                    if student is not None:
                        # Check if an AdmitCardDesign exists for the specified student and exam
                        admit_card = AdmitCardDesign.objects.filter(
                            student=student, exam=exam).first()

                        if admit_card is not None:
                            serializer = AdmitCardDesignSerializer(admit_card)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": "Admit Card not found for the specified student and exam"}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"error": "Student not found in the specified class"}, status=status.HTTP_404_NOT_FOUND)
                except Exam.DoesNotExist:
                    return Response({"error": "Exam not found in the specified group"}, status=status.HTTP_404_NOT_FOUND)
        except ExamGroup.DoesNotExist:
            return Response({"error": "ExamGroup not found"}, status=status.HTTP_404_NOT_FOUND)
        
        

class StudentMarksheetSearchView(viewsets.ViewSet):
    serializer_class = MarksheetDesignSerializer

    @action(detail=False, methods=['post'])
    def search_marksheet(self, request):
        group_id = request.data.get('group_id')
        exam_id = request.data.get('exam_id')
        class_id = request.data.get('class_id')
        student_id = request.data.get('student_id')

        try:
            # Query the ExamGroup by its ID
            exam_group = ExamGroup.objects.get(id=group_id)
            exams = exam_group.exam.all()  # Access the related exams from the ExamGroup instance

            # Check if both group_id and exam_id are provided and exist in the group
            if group_id is not None and exam_id is not None:
                try:
                    exam = exams.get(id=exam_id)

                    # Check if the specified student is in the specified class
                    student = Student.objects.filter(
                        id=student_id, current_class_id=class_id).first()

                    if student is not None:
                        # Check if a MarksheetDesign exists for the specified student and exam
                        marksheet = MarksheetDesign.objects.filter(
                            student=student, exam=exam).first()

                        if marksheet is not None:
                            serializer = MarksheetDesignSerializer(marksheet)
                            return Response(serializer.data, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": "Marksheet not found for the specified student and exam"}, status=status.HTTP_404_NOT_FOUND)
                    else:
                        return Response({"error": "Student not found in the specified class"}, status=status.HTTP_404_NOT_FOUND)
                except Exam.DoesNotExist:
                    return Response({"error": "Exam not found in the specified group"}, status=status.HTTP_404_NOT_FOUND)
        except ExamGroup.DoesNotExist:
            return Response({"error": "ExamGroup not found"}, status=status.HTTP_404_NOT_FOUND)
