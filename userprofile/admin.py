from django.contrib import admin
from .models import Userprofile, ConversationMessage, WithdrawalRequest
from import_export.admin import ImportExportModelAdmin

admin.site.register(Userprofile, ImportExportModelAdmin)
admin.site.register(ConversationMessage, ImportExportModelAdmin)

@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('userprofile', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['approve_withdrawals', 'deny_withdrawals']

    def save_model(self, request, obj, form, change):
        if change:  # Only send notification if the object is being updated
            original = WithdrawalRequest.objects.get(pk=obj.pk)
            if original.status != obj.status:
                obj.notify_user()
        super().save_model(request, obj, form, change)

    def approve_withdrawals(self, request, queryset):
        updated = queryset.update(status='approved')
        for withdrawal in queryset:
            withdrawal.notify_user()
        self.message_user(request, f"{updated} withdrawal requests have been approved and users notified.")
    
    approve_withdrawals.short_description = "Approve selected withdrawal requests"

    def deny_withdrawals(self, request, queryset):
        updated = queryset.update(status='denied')
        for withdrawal in queryset:
            withdrawal.notify_user()
        self.message_user(request, f"{updated} withdrawal requests have been denied and users notified.")
    
    deny_withdrawals.short_description = "Deny selected withdrawal requests"