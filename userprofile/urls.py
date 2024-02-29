from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("task/<int:task_id>/", views.view_task, name="view_task"),
    path('recommend_tasks/', views.recommend_tasks, name='recommended-tasks'),
    path("application/<int:application_id>/", views.view_application, name="application"),
    path('view_application/<int:application_id>/', views.view_application, name='view_application'),
    path('edit_application/<int:application_id>/', views.edit_application, name='edit_application'),
    path('approve/<int:application_id>/', views.approve_application, name='approve_application'),
]


