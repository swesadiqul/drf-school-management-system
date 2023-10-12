from django.urls import path 
from student.views.student import StudentListCreateView

app_name = 'student'

urlpatterns = [
    path('create-list-student/', StudentListCreateView.as_view(), name='student-list-create')
]



