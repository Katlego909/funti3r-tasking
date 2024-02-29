from userprofile.models import Userprofile

def update_user_earnings(application):
    if application.approved and application.assigned and application.created_by == application.task.assigned_to:
        user_profile = Userprofile.objects.get(user=application.task.assigned_to)
        amount = application.calculate_task_amount()
        user_profile.earnings += amount
        user_profile.save()