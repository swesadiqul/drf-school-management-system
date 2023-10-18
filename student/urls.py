from django.urls import path, include
from .views.student import StudentListView, StudentAdmissionListCreateView, SectionListCreateView, ClassListCreateView, PromoteStudentListCreateView
from .views.parent import ParentListView
from .views.fees import FeesGroupListCreateView, FeesTypeListCreateView, FeesDiscountListCreateView, FeesMasterListCreateView

app_name = 'student'

urlpatterns = [
    path('create-list-student-admission/', StudentAdmissionListCreateView.as_view(), name='student_admission_list_create'),
    path('create-list-section/', SectionListCreateView.as_view(), name='section_list_create'),
    path('create-list-class/', ClassListCreateView.as_view(), name='class_list_create'),
    
    # Student List
    path('list-students/', StudentListView.as_view({'get': 'list_students'}), name='list_students'),
    path('list-disabled-students/', StudentListView.as_view({'get': 'list_disabled_students'}), name='list_disabled_students'),
    path('list-enabled-students/', StudentListView.as_view({'get': 'list_enabled_students'}), name='list_enabled_students'),
    
    
    
    path('parent-list/', ParentListView.as_view(), name='parent_list'),
    
    # Promote Student
    path('promote-student/', PromoteStudentListCreateView.as_view({'post': 'promote_student'}), name='promote_student'),
    path('promote-all-students/', PromoteStudentListCreateView.as_view({'post': 'promote_all_students'}), name='promote_all_students'),
    
    
    # Stuent Fees
    path('create-fees-group/', FeesGroupListCreateView.as_view({'post': 'create_fee_group'}), name='create_fees_group'),
    path('list-fees-group/', FeesGroupListCreateView.as_view({'get': 'fees_group_list'}), name='fees_group_list'),
    
    path('create-fees-type/', FeesTypeListCreateView.as_view({'post': 'create_fee_type'}), name='create_fee_type'),
    path('list-fees-type/', FeesTypeListCreateView.as_view({'get': 'fees_type_list'}), name='fees_type_list'),
    
    path('create-fees-discount/', FeesDiscountListCreateView.as_view({'post': 'create_fee_discount'}), name='create_fee_discount'),
    path('list-fees-discount/', FeesDiscountListCreateView.as_view({'get': 'fees_discount_list'}), name='fees_discount_list'),
    
    path('create-fees-master/', FeesMasterListCreateView.as_view({'post': 'create_fee_master'}), name='create_fee_master'),
    path('list-fees-master/', FeesMasterListCreateView.as_view({'get': 'fees_master_list'}), name='fees_master_list'),
]



