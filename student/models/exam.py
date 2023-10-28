from django.db import models
from .student import Subject

class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    subject = models.ManyToManyField('Subject')
    date_from = models.DateField()
    start_time = models.TimeField()
    duration = models.DurationField()
    room_no = models.CharField(max_length=20)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    min_marks = models.DecimalField(max_digits=5, decimal_places=2) 

    def __str__(self):
        return self.exam_name
    
class ExamType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name
    
class ExamGroup(models.Model):
    group_name = models.CharField(max_length=100)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    exam = models.ManyToManyField('Exam')
    description = models.TextField(blank=True, null=True)
    no_of_exam = models.IntegerField(editable=False, default=0) 

    def __str__(self):
        return self.group_name
    
    def save(self, *args, **kwargs):
         super(ExamGroup, self).save(*args, **kwargs)
         self.no_of_exam = self.exam.count()
         super(ExamGroup, self).save(*args, **kwargs)

class AdmitCardDesign(models.Model):
    template_name = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    exam_center = models.CharField(max_length=100)
    footer_text = models.TextField()
    left_logo = models.ImageField(upload_to='admit_card_logos/')
    right_logo = models.ImageField(upload_to='admit_card_logos/')
    sign = models.ImageField(upload_to='admit_card_signs/')
    background_image = models.ImageField(upload_to='admit_card_backgrounds')
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return self.template_name
    
class MarksheetDesign(models.Model):
    template_name = models.CharField(max_length=100)
    heading = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100)
    exam_center = models.CharField(max_length=100)
    footer_text = models.TextField()
    body_text = models.TextField()
    header_image = models.ImageField(upload_to='mark_sheet_header/')
    left_logo = models.ImageField(upload_to='mark_sheet_logos/')
    right_logo = models.ImageField(upload_to='mark_sheet_logos/')
    left_sign = models.ImageField(upload_to='mark_sheet_signs/')
    middle_sign = models.ImageField(upload_to='mark_sheet_signs/')
    right_sign = models.ImageField(upload_to='mark_sheet_signs/')
    background_image = models.ImageField(upload_to='mark_sheet_backgrounds')
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return self.template_name
    
class MarksGrade(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    grade_name = models.CharField(max_length=10)
    percent_upto = models.DecimalField(max_digits=5, decimal_places=2)
    percent_from = models.DecimalField(max_digits=5, decimal_places=2)
    grade_point = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.grade_name
    
class MarksDivision(models.Model):
    division_name = models.CharField(max_length=50)
    percent_from = models.DecimalField(max_digits=5, decimal_places=2)
    percent_upto = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.division_name