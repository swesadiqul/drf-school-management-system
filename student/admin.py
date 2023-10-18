from django.contrib import admin
from .models.student import StudentAdmission, Class, Section, Subject, PromoteStudents, Student, StudentCategory, DisableReason
from .models.parent import Parent
from .models.fees import FeesGroup, FeesType, FeesDiscount, FeesMaster, Payment, FeesCollect

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
admin.site.register(FeesGroup)
admin.site.register(FeesType)
admin.site.register(FeesDiscount)
admin.site.register(FeesMaster)
admin.site.register(Payment)
admin.site.register(FeesCollect)