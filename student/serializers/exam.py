from rest_framework import serializers
from ..models.exam import ExamType, Exam, ExamGroup, MarksGrade, MarksDivision, AdmitCardDesign, MarksheetDesign
from ..models.student import Student


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    subject_info = serializers.SerializerMethodField()

    def get_subject_info(self, obj):
        subject_data = []
        for subject in obj.subject.all():
            subject_data.append({
                "subject_name": subject.subject_name,
                "subject_code": subject.subject_code,
            })
        return subject_data

    class Meta:
        model = Exam
        fields = '__all__'


class ExamGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamGroup
        fields = '__all__'
        optional_fields = ['description', 'no_of_exam']


class MarksGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarksGrade
        fields = '__all__'
        optional_fields = ['description']


class MarksDivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarksDivision
        fields = '__all__'

class ExamAdmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'exam_name']

class StudentAdmitSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()

    def get_student_name(self, obj):
        return obj.user.get_full_name()

    class Meta:
        model = Student
        fields = ['id', 'student_name']

class AdmitCardDesignSerializer(serializers.ModelSerializer):
    exam_name = ExamAdmitSerializer(source='exam', read_only=True)
    student_name = StudentAdmitSerializer(source='student', read_only=True)
    
    class Meta:
        model = AdmitCardDesign
        fields = '__all__'
        

class MarksheetDesignSerializer(serializers.ModelSerializer):
    exam_name = ExamAdmitSerializer(source='exam', read_only=True)
    student_name = StudentAdmitSerializer(source='student', read_only=True)

    class Meta:
        model = MarksheetDesign
        fields = '__all__'
