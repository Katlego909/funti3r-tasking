from django.contrib import admin
from .models import Notification
from import_export.admin import ImportExportModelAdmin

admin.site.register(Notification, ImportExportModelAdmin)
