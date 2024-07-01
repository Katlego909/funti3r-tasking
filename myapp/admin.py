from django.contrib import admin
from .models import Ticket
from import_export.admin import ImportExportModelAdmin

admin.site.register(Ticket, ImportExportModelAdmin)
