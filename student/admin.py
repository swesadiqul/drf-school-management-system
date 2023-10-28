from django.contrib import admin
from .models.student import *
from .models.parent import Parent
from .models.fees import *
from .models.exam import *

# Register your models here.
admin.site.register(StudentAdmission)
admin.site.register(Class)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(PromoteStudents)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(StudentCategory)
admin.site.register(DisableReason)

## Fees
admin.site.register(FeesGroup)
admin.site.register(FeesType)
admin.site.register(FeesDiscount)
admin.site.register(FeesMaster)
admin.site.register(Payment)
admin.site.register(FeesCollect)

## Exam
admin.site.register(Exam)
admin.site.register(ExamType)
admin.site.register(ExamGroup)
admin.site.register(AdmitCardDesign)
admin.site.register(MarksGrade)
