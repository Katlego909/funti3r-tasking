from django.contrib import admin
from .models import  Category, Skill,Task, Application
from import_export.admin import ImportExportModelAdmin

admin.site.register(Category, ImportExportModelAdmin)
admin.site.register(Skill, ImportExportModelAdmin)
admin.site.register(Task, ImportExportModelAdmin)
admin.site.register(Application, ImportExportModelAdmin)
