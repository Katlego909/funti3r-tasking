from django.contrib import admin
from django.contrib import messages
from .models import Category, Skill, Task, Application
from userprofile.models import Userprofile  # Ensure this import is correct
from import_export.admin import ImportExportModelAdmin

admin.site.register(Category, ImportExportModelAdmin)
admin.site.register(Skill, ImportExportModelAdmin)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'created_at')
    actions = ['mark_as_complete']

    def mark_as_complete(self, request, queryset):
        for task in queryset:
            if task.status != 'completed':  # Ensure the status 'completed' is valid or define it in your CHOICES_STATUS
                task.status = 'completed'  # Mark the task as completed
                if task.assigned_to:
                    user_profile = task.assigned_to.userprofile  # Get the assigned user's profile
                    user_profile.earnings += task.amount  # Update the user's earnings
                    user_profile.save()
                    task.save()
                    self.message_user(request, f"Task '{task.title}' marked as complete and earnings updated for {task.assigned_to.username}.")
                else:
                    self.message_user(request, f"Task '{task.title}' is not assigned to any user.", level=messages.WARNING)
            else:
                self.message_user(request, f"Task '{task.title}' is already marked as completed.", level=messages.WARNING)

    mark_as_complete.short_description = "Mark selected tasks as complete and update earnings"

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('task', 'created_by', 'approval_status', 'created_at')
    actions = ['approve_application']

    def approve_application(self, request, queryset):
        for application in queryset:
            if application.approval_status == Application.PENDING:
                application.approval_status = Application.APPROVED
                application.approved_by = request.user
                application.save()

                # Assign earnings to the user
                user_profile = application.created_by.userprofile
                user_profile.earnings += application.task.amount
                user_profile.save()

                self.message_user(request, f"Approved application for {application.created_by.username}.")
            else:
                self.message_user(request, f"Application for {application.created_by.username} is already {application.approval_status}.", level=messages.ERROR)

    approve_application.short_description = "Approve selected applications"
