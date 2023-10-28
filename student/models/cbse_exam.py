from django.db import models


class Term(models.Model):
    term_name = models.CharField(max_length=100)
    term_code = models.CharField(max_length=10)
    description = models.TextField()

    def __str__(self):
        return self.term_name


class CBSE_Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    is_exam_published = models.BooleanField(default=False)
    is_result_published = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    term_name = models.ForeignKey(Term, on_delete=models.CASCADE)
    class_name = models.ForeignKey('Class', on_delete=models.CASCADE)
    section_name = models.ManyToManyField('Section')
    assessment_name = models.ForeignKey('Assessment', on_delete=models.CASCADE)
    grade_name = models.ForeignKey('Grade', on_delete=models.CASCADE)
    # student = models.ManyToManyField('Student')
    # exam = models.ManyToManyField('Exam_Mark')
    created_at = models.DateTimeField()

    def __str__(self):
        return self.exam_name


class Exam_Mark(models.Model):
    subject = models.ManyToManyField('Subject')
    theory_mark = models.DecimalField(max_digits=5, decimal_places=2)
    practical_mark = models.DecimalField(max_digits=5, decimal_places=2)
    assignment_mark = models.DecimalField(max_digits=5, decimal_places=2)
    is_theory_absent = models.BooleanField()
    is_practical_absent = models.BooleanField()
    is_assignment_absent = models.BooleanField()
    total_mark = models.DecimalField(max_digits=5, decimal_places=2)
    remark = models.TextField()
    note = models.TextField()


class Assessment(models.Model):
    assess_name = models.CharField(max_length=100)
    assess_description = models.TextField()
    assessment_fields = models.ManyToManyField('AssessmentField')

    def __str__(self):
        return self.assess_name


class AssessmentField(models.Model):
    assess_type = models.CharField(max_length=100)
    assess_code = models.CharField(max_length=10)
    maximum_marks = models.DecimalField(max_digits=5, decimal_places=2)
    pass_percent = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.assess_type} - {self.assess_code}"


class Template(models.Model):
    template_name = models.CharField(max_length=100)
    class_name = models.ForeignKey('Class', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    marksheet_type_choices = [
        ('Landscape', 'Landscape'),
        ('Portrait', 'Portrait'),
    ]
    marksheet_type = models.CharField(
        max_length=9, choices=marksheet_type_choices)
    school_name = models.CharField(max_length=100)
    exam_center = models.CharField(max_length=100)
    printing_date = models.DateField()
    header_image = models.ImageField(upload_to='template_header/')
    footer_text = models.TextField()
    left_sign = models.ImageField(upload_to='template_signs/')
    middle_sign = models.ImageField(upload_to='template_signs/')
    right_sign = models.ImageField(upload_to='template_signs/')
    background_image = models.ImageField(upload_to='template_backgrounds')
    template_description = models.TextField(blank=True, null=True)


class Observation(models.Model):
    observation_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parameter = models.ForeignKey(
        'ObservationParameter', on_delete=models.CASCADE)
    max_mark = models.DecimalField(max_digits=5, decimal_places=2)


class ObservationParameter(models.Model):
    param_name = models.CharField(max_length=100)


class AssignObservation(models.Model):
    observation = models.ForeignKey('Observation', on_delete=models.CASCADE)
    term = models.ForeignKey('Term', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)


class ExamGrade(models.Model):
    grade_title = models.CharField(max_length=100)
    description = models.TextField()
    grade_fields = models.ForeignKey(
        'ExamGradeField', on_delete=models.CASCADE)


class ExamGradeField(models.Model):
    grade_name = models.CharField(max_length=100)
    max_percent = models.DecimalField(max_digits=5, decimal_places=2)
    min_percent = models.DecimalField(max_digits=5, decimal_places=2)
    remark = models.TextField()
