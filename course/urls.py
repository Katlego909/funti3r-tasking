from django.urls import path
from . import views

urlpatterns = [
    path('course_list/', views.course_list, name='course_list'),
    path('progress/', views.learner_progress, name='progress'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/chapters/<int:chapter_id>/', views.chapter_detail, name='chapter_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/resource/<int:resource_id>/', views.lesson_resource, name='lesson_resource'),
    path('course/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('lesson/<int:lesson_id>/mark_complete/', views.mark_as_complete, name='mark_as_complete'),
]
