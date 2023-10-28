from django.urls import path, include
from .views.student import StudentListView, StudentAdmissionListCreateView, SectionListCreateView, ClassListCreateView, PromoteStudentListCreateView, StudentListClsSecViewSet
from .views.parent import ParentListView
from .views.fees import FeesGroupListCreateView, FeesTypeListCreateView, FeesDiscountListCreateView, FeesMasterListCreateView, FeesCollectViewSet, PaymentDetailsViewSet, FeesDueMessageSentViewSet
from .views.exam import ExamGroupViewSet, ExamTypeViewSet, ExamViewSet, ExamScheduleViewSet , MarksGradeViewSet, MarksDivisionViewSet, AdmitCardDesignViewSet, MarksheetDesignViewSet, StudentAdmitCardSearchView, StudentMarksheetSearchView

app_name = 'student'


urlpatterns = [
    path('create-list-student-admission/', StudentAdmissionListCreateView.as_view(),
         name='student_admission_list_create'),
    path('create-list-section/', SectionListCreateView.as_view(),
         name='section_list_create'),
    path('create-list-class/', ClassListCreateView.as_view(),
         name='class_list_create'),

    # Student List
    path('list-students/',
         StudentListView.as_view({'get': 'list_students'}), name='list_students'),
    path('list-disabled-students/', StudentListView.as_view(
        {'get': 'list_disabled_students'}), name='list_disabled_students'),
    path('list-enabled-students/', StudentListView.as_view(
        {'get': 'list_enabled_students'}), name='list_enabled_students'),

    path('get-all-students-cls-sec/', StudentListClsSecViewSet.as_view(
    {'post': 'get_all_students_cls_sec'}), name='get_all_students_cls_sec'),

    path('parent-list/', ParentListView.as_view(), name='parent_list'),

    # Promote Student
    path('promote-student/', PromoteStudentListCreateView.as_view(
        {'post': 'promote_student'}), name='promote_student'),
    path('promote-all-students/', PromoteStudentListCreateView.as_view(
        {'post': 'promote_all_students'}), name='promote_all_students'),


    # Stuent Fees
    path('create-fees-group/', FeesGroupListCreateView.as_view(
        {'post': 'create_fee_group'}), name='create_fees_group'),
    path('list-fees-group/', FeesGroupListCreateView.as_view(
        {'get': 'fees_group_list'}), name='fees_group_list'),

    path('create-fees-type/', FeesTypeListCreateView.as_view(
        {'post': 'create_fee_type'}), name='create_fee_type'),
    path('list-fees-type/', FeesTypeListCreateView.as_view(
        {'get': 'fees_type_list'}), name='fees_type_list'),

    path('create-fees-discount/', FeesDiscountListCreateView.as_view(
        {'post': 'create_fee_discount'}), name='create_fee_discount'),
    path('list-fees-discount/', FeesDiscountListCreateView.as_view(
        {'get': 'fees_discount_list'}), name='fees_discount_list'),

    path('create-fees-master/', FeesMasterListCreateView.as_view(
        {'post': 'create_fee_master'}), name='create_fee_master'),
    path('list-fees-master/', FeesMasterListCreateView.as_view(
        {'get': 'fees_master_list'}), name='fees_master_list'),
    
    path('collect-fees/<int:student_id>/', FeesCollectViewSet.as_view({'post': 'collect_fees'}), name='collect_fees'),
    
    path('get-payment-details/', PaymentDetailsViewSet.as_view({'post': 'get_payment_details'}), name='get_payment_details'),
    
    path('sent-fee-due-message/', FeesDueMessageSentViewSet.as_view({'post': 'fees_due_message_sent_students'}), name='fees_due_message_sent_students'),
    
    
    # Stuent Exam
    path('list-exam-types/', ExamTypeViewSet.as_view({'get': 'get_exam_types'}), name='get_exam_types'),
    path('create-exam-type/', ExamTypeViewSet.as_view({'post': 'create_exam_type'}), name='create_exam_type'),
    
    path('list-exams/', ExamViewSet.as_view({'get': 'get_exams'}), name='get_exams'),
    path('create-exam/', ExamViewSet.as_view({'post': 'create_exam'}), name='create_exam'),
    
    path('list-exam-groups/', ExamGroupViewSet.as_view({'get': 'get_exam_groups'}), name='get_exam_groups'),
    path('create-exam-group/', ExamGroupViewSet.as_view({'post': 'create_exam_group'}), name='create_exam_group'),
    
    path('list-exam-schedule/', ExamScheduleViewSet.as_view({'post': 'group_exams_schedule'}), name='group_exams_schedule'),
    
    path('list-mark-grades/', MarksGradeViewSet.as_view({'get': 'list_marks_grades'}), name='list_marks_grades'),
    path('create-mark-grade/', MarksGradeViewSet.as_view({'post': 'create_marks_grade'}), name='create_marks_grade'),
    path('list-grades-by-examtype/', MarksGradeViewSet.as_view({'post': 'get_grades_by_exam_type'}), name='get_grades_by_exam_type'),
    
    path('list-mark-divisions/', MarksDivisionViewSet.as_view({'get': 'list_marks_divisions'}), name='list_marks_divisions'),
    path('create-mark-division/', MarksDivisionViewSet.as_view({'post': 'create_marks_division'}), name='create_marks_division'),

    path('create-admit-card/', AdmitCardDesignViewSet.as_view({'post': 'generate_admit_card'}), name='generate_admit_card'),
    path('list-admit-card/', AdmitCardDesignViewSet.as_view({'get': 'get_admit_card'}), name='get_admit_card'),
    
    path('create-marksheet-card/', MarksheetDesignViewSet.as_view({'post': 'generate_marksheet_design'}), name='generate_marksheet_design'),
    path('list-marksheet-card/', MarksheetDesignViewSet.as_view({'get': 'get_marksheet_design'}), name='get_marksheet_design'),
    
    path('search-admit-card/', StudentAdmitCardSearchView.as_view({'post': 'search_admit_card'}), name='search_admit_card'),
    
    path('search-marksheet/', StudentMarksheetSearchView.as_view({'post': 'search_marksheet'}), name='search_marksheet'),
]
