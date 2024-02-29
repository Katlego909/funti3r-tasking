from django.contrib import admin
from .models import Category, Course, Lesson, LessonResource, Enrollment, Progress, Chapter, Resource

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(LessonResource)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(Chapter)
admin.site.register(Resource)


