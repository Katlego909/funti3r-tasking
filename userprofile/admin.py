from django.contrib import admin
from .models import Userprofile, ConversationMessage
from import_export.admin import ImportExportModelAdmin

admin.site.register(Userprofile, ImportExportModelAdmin)
admin.site.register(ConversationMessage, ImportExportModelAdmin)
