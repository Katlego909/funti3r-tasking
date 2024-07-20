from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from notifications.utilities import create_notification
from tasks.models import Application, Task
from .models import ConversationMessage, WithdrawalRequest  
from .forms import UserProfileForm, UpgradeAccountForm
from django.contrib import messages
from tasks.forms import ApplicationForm
from django.core.exceptions import PermissionDenied
from .decorators import paid_account_required
from decimal import Decimal
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

# User Profile Views
@login_required
def profile(request): 
    return render(request, "userprofile/profile.html", {'userprofile': request.user.userprofile})

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.has_changed() and form.is_valid():
            form.save()
            new_username = form.cleaned_data['username']
            if request.user.username != new_username:
                request.user.username = new_username
            return redirect('profile')
    else:
        initial_data = {'industry': user_profile.industry} if user_profile.industry else {}
        form = UserProfileForm(instance=user_profile, initial=initial_data)

    return render(request, 'userprofile/edit_profile.html', {'form': form})

# Task Views
@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.status = 'completed'
        user_profile = request.user.userprofile
        user_profile.earnings += task.amount
        user_profile.save()
        task.save()
        messages.success(request, "Task marked as complete and earnings updated.")
        return redirect('dashboard')

    return render(request, 'userprofile/complete_task.html', {'task': task})

@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, created_by=request.user)
    return render(request, "userprofile/view_task.html", {"task": task})

# Withdrawal Views
@login_required
def request_withdrawal(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        user_profile = request.user.userprofile

        if amount <= 0 or amount > user_profile.earnings:
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('request_withdrawal')

        WithdrawalRequest.objects.create(
            userprofile=user_profile,
            amount=amount,
            status='pending'
        )

        user_profile.earnings -= amount
        user_profile.save()
        notify_admin(user_profile, amount)

        messages.success(request, "Withdrawal request submitted successfully!")
        return redirect('withdrawal_success')

    return render(request, 'userprofile/request_withdrawal.html')

@login_required
def withdrawal_success(request):
    return render(request, 'userprofile/withdrawal_success.html')

@login_required
@staff_member_required
def approve_withdrawal(request, withdrawal_id):
    withdrawal = get_object_or_404(WithdrawalRequest, pk=withdrawal_id)

    if request.method == 'POST':
        withdrawal.status = 'approved'
        withdrawal.save()
        notify_user_withdrawal_status(withdrawal.userprofile, withdrawal.amount, 'approved')

        messages.success(request, "Withdrawal approved successfully!")
        return redirect('withdrawals')

    return render(request, 'userprofile/approve_withdrawal.html', {'withdrawal': withdrawal})

@login_required
@staff_member_required
def reject_withdrawal(request, withdrawal_id):
    withdrawal = get_object_or_404(WithdrawalRequest, pk=withdrawal_id)
    withdrawal.status = 'rejected'
    withdrawal.save()
    notify_user_withdrawal_status(withdrawal.userprofile, withdrawal.amount, 'rejected')
    messages.success(request, "Withdrawal rejected successfully!")
    return redirect('withdrawals')

@staff_member_required
def list_withdrawals(request):
    withdrawals = WithdrawalRequest.objects.all()
    return render(request, 'userprofile/list_withdrawals.html', {'withdrawals': withdrawals})

@login_required
def view_withdrawals(request):
    withdrawals = WithdrawalRequest.objects.all()
    return render(request, 'userprofile/withdrawals.html', {'withdrawals': withdrawals})

# Account Upgrade/Downgrade Views
@login_required
def upgrade_account(request):
    if request.method == 'POST':
        form = UpgradeAccountForm(request.POST)
        if form.is_valid():
            user_profile = request.user.userprofile
            user_profile.account_type = 'paid'
            user_profile.save()
            return redirect('profile')
    else:
        form = UpgradeAccountForm()

    return render(request, 'userprofile/upgrade_account.html', {'form': form})

@login_required
def downgrade_account(request):
    user_profile = request.user.userprofile
    user_profile.account_type = 'free'
    user_profile.save()
    return redirect('profile')

# Notification Functions
def notify_admin(user_profile, amount):
    subject = "New Withdrawal Request"
    message = render_to_string('userprofile/request_withdrawal.html', {'user_profile': user_profile, 'amount': amount})
    email = EmailMultiAlternatives(subject, message, 'your_organization@example.com', ['admin@example.com'])
    email.attach_alternative(message, "text/html")
    email.send()

def notify_user_withdrawal_status(user_profile, amount, status):
    subject = f"Withdrawal {status.capitalize()}"
    message = render_to_string('userprofile/withdrawal_status.html', {'user_profile': user_profile, 'amount': amount, 'status': status})
    email = EmailMultiAlternatives(subject, message, 'your_organization@example.com', [user_profile.user.email])
    email.attach_alternative(message, "text/html")
    email.send()

# Application Views
@login_required
def view_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if not request.user.is_superuser and request.user != application.created_by:
        raise PermissionDenied()

    if request.method == "POST":
        if 'delete_application' in request.POST:
            application.delete()
            messages.success(request, 'Application deleted successfully.')
            return redirect('profile')
        elif 'approve_application' in request.POST:
            admin_user = request.user
            assigned_user = application.created_by
            try:
                message = application.approve_and_assign(admin_user, assigned_user)
                messages.success(request, message)
            except ValueError as e:
                messages.error(request, str(e))
            return redirect('profile')

        content = request.POST.get("content")
        if content:
            ConversationMessage.objects.create(application=application, content=content, created_by=request.user)
            create_notification(request, application.created_by, "message", extra_id=application.id)
            return redirect('application', application_id=application_id)

        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('view_application', application_id=application_id)

    else:
        form = ApplicationForm(instance=application)

    return render(request, "userprofile/view_application.html", {"application": application, "form": form})

def edit_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id, created_by=request.user)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('view_application', application_id=application_id)
    else:
        form = ApplicationForm(instance=application)

    return render(request, "userprofile/edit_application.html", {"form": form, "application": application})

@login_required
@paid_account_required
def recommend_tasks(request):
    user_profile = request.user.userprofile

    if user_profile.industry:
        recommended_tasks = Task.objects.filter(category__name=user_profile.industry, status=Task.ACTIVE)
        context = {
            'user_profile': user_profile,
            'recommended_tasks': recommended_tasks,
        }
        return render(request, 'userprofile/recommend_tasks.html', context)
    else:
        return render(request, 'userprofile/no_industry_selected.html')

def approve_application(request, application_id):
    application = Application.objects.get(pk=application_id)
    admin_user = request.user
    assigned_user = application.assigned_to
    approved_message = application.approve_and_assign(admin_user, assigned_user)
    messages.success(request, approved_message)
    return redirect('home')
