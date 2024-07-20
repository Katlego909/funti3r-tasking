from django.urls import path
from . import views  # Import all views from views.py
from .views import complete_task, request_withdrawal, withdrawal_success, list_withdrawals, approve_withdrawal, reject_withdrawal, view_withdrawals

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("task/<int:task_id>/", views.view_task, name="view_task"),
    path('recommend_tasks/', views.recommend_tasks, name='recommended-tasks'),
    path("application/<int:application_id>/", views.view_application, name="application"),
    path('view_application/<int:application_id>/', views.view_application, name='view_application'),
    path('edit_application/<int:application_id>/', views.edit_application, name='edit_application'),
    path('approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('upgrade/', views.upgrade_account, name='upgrade_account'),
    path('downgrade/', views.downgrade_account, name='downgrade_account'),
    path('complete-task/<int:task_id>/', complete_task, name='complete_task'),  # Ensure this is included
    path('request-withdrawal/', request_withdrawal, name='request_withdrawal'),  # Ensure this is included
    path('request-withdrawal/', request_withdrawal, name='request_withdrawal'),
    path('withdrawal-success/', withdrawal_success, name='withdrawal_success'),
    path('withdrawals/', list_withdrawals, name='list_withdrawals'),
    path('withdrawals/approve/<int:withdrawal_id>/', approve_withdrawal, name='approve_withdrawal'),
     path('withdrawals/reject/<int:withdrawal_id>/', reject_withdrawal, name='reject_withdrawal'),
      path('withdrawals/', view_withdrawals, name='withdrawals'),
]

