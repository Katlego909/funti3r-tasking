from django.contrib import admin
from .models import Category, Course, Lesson, LessonResource, Enrollment, Progress, Chapter, Resource

import data_wizard

from import_export.admin import ImportExportModelAdmin

admin.site.register(Category, ImportExportModelAdmin)
admin.site.register(Course, ImportExportModelAdmin)

data_wizard.register(Course)

admin.site.register(Lesson, ImportExportModelAdmin)
admin.site.register(LessonResource, ImportExportModelAdmin)
admin.site.register(Enrollment, ImportExportModelAdmin)
admin.site.register(Progress, ImportExportModelAdmin)
admin.site.register(Chapter, ImportExportModelAdmin)
admin.site.register(Resource, ImportExportModelAdmin)


