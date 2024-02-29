from django.urls import path

from tasks.api import api_search
from . import views

urlpatterns = [
    path('api/search', api_search, name="api_search" ),
    path('tasks/', views.tasks, name="tasks" ),
    path('add_task/', views.add_task, name="add_task" ),
    path('approve_and_assign_task/<int:task_id>/', views.approve_and_assign_task, name='approve_and_assign_task'),
    path('apply_for_task/<int:task_id>/', views.apply_for_task, name="apply" ),
    path('delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('tasks/<int:task_id>/', views.task_detail, name="task_detail" ),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('archive/', views.archive_or_favorite_page, {'status': 'archived'}, name='archive_page'),
    path('favorite/', views.archive_or_favorite_page, {'status': 'favorite'}, name='favorite_page'),
    path('toggle_favorite/<int:task_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('approve_and_assign/<int:application_id>/', views.approve_and_assign_application, name='approve_and_assign'),
]
