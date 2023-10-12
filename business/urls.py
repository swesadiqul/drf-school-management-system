from django.urls import path
from .views.business import CreateBusinessAPIView, BusinessListAPIView, CreateBusinessBranchAPIView, BusinessBranchesListView
                             
from .views.business_admin import BusinessAdminListAPIView, BusinessBranchAdminAPIView
from .views.unisersal_entity import TypeListCreateAPIView, TypeDetailAPIView, UniversalEntitiesListCreateAPIView, UniversalEntitiesDetailAPIView    

app_name = 'business'

urlpatterns = [
    
    path('create-business/', CreateBusinessAPIView.as_view(), name='create_business'),
    path('businesses/', BusinessListAPIView.as_view(), name='business_list'),
    path('business-admins/', BusinessAdminListAPIView.as_view(), name='business_admin_list'),
    path('create-branch/', CreateBusinessBranchAPIView.as_view(), name='create_branch'),
    path('business-branches/<int:business_id>/', BusinessBranchesListView.as_view(), name='business_branch_list'),
    path('business-branch-admin/<int:business_id>/', BusinessBranchAdminAPIView.as_view(), name='business_branch_admin_list'),
    
    # Universal Entities
    
    path('<int:business_id>/types/', TypeListCreateAPIView.as_view(), name='type_list_create'),
    path('<int:business_id>/types/<int:type_id>/', TypeDetailAPIView.as_view(), name='type_detail'),
    path('universal-entities/', UniversalEntitiesListCreateAPIView.as_view(), name='universal-entities-list-create'),
    path('universal-entities/<int:universal_id>/', UniversalEntitiesDetailAPIView.as_view(), name='universal-entities-detail'),
    
]



