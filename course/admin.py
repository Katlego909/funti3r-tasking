from django.contrib import admin
from .models import Category, Course, Lesson, LessonResource, Enrollment, Progress, Chapter, Resource

import data_wizard

admin.site.register(Category)
admin.site.register(Course)

data_wizard.register(Course)

admin.site.register(Lesson)
admin.site.register(LessonResource)
admin.site.register(Enrollment)
admin.site.register(Progress)
admin.site.register(Chapter)
admin.site.register(Resource)


