from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from notifications.utilities import create_notification
from tasks.models import Application, Task
from .models import ConversationMessage
from .forms import UserProfileForm, UpgradeAccountForm
from django.contrib import messages
from tasks.forms import ApplicationForm
from django.core.exceptions import PermissionDenied
from .decorators import paid_account_required

@login_required
def profile(request): 
    return render(request, "userprofile/profile.html", {'userprofile': request.user.userprofile})

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

def user_profile_view(request):
    user = request.user
    application_count = user.userprofile.get_application_count()
    
    context = {
        'application_count': application_count,
    }
    
    return render(request, 'user_profile.html', context)

@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.has_changed() and form.is_valid():
            form.save()

            # Update the username
            new_username = form.cleaned_data['username']

            # Check if the username has changed
            if request.user.username != new_username:
                # Update the username using Django's authentication system
                request.user.username = new_username
                # request.user.save()
            return redirect('profile')  # Redirect to the user's profile page
    else:
        # Get the selected industry if it exists
        initial_data = {'industry': user_profile.industry} if user_profile.industry else {}
        form = UserProfileForm(instance=user_profile, initial=initial_data)

    return render(request, 'userprofile/edit_profile.html', {'form': form})

@login_required
@paid_account_required
def recommend_tasks(request):
    user_profile = request.user.userprofile

    if user_profile.industry:
        # Retrieve tasks based on the selected industry
        recommended_tasks = Task.objects.filter(category__name=user_profile.industry, status=Task.ACTIVE)

        context = {
            'user_profile': user_profile,
            'recommended_tasks': recommended_tasks,
        }
        return render(request, 'userprofile/recommend_tasks.html', context)
    else:
        # Handle the case when the user has not selected an industry
        return render(request, 'userprofile/no_industry_selected.html')

@login_required
def view_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    
    # Check permissions to view the application status
    if not request.user.is_superuser and request.user != application.created_by:
        raise PermissionDenied()

    if request.method == "POST":
        if 'delete_application' in request.POST:
            # Delete application if requested
            application.delete()
            messages.success(request, 'Application deleted successfully.')
            return redirect('profile')  # Redirect to user's profile or any appropriate page after deletion
            
        elif 'approve_application' in request.POST:
            # Approve and assign application
            admin_user = request.user
            assigned_user = application.created_by
            try:
                # Call the approve_and_assign method to approve and assign the application
                message = application.approve_and_assign(admin_user, assigned_user)
                messages.success(request, message)
            except ValueError as e:
                messages.error(request, str(e))
                
            # Redirect to user's profile after approval and assignment
            return redirect('profile')  

        # Process form submission (e.g., sending a message or editing the application)
        content = request.POST.get("content")
        if content:
            # Create a conversation message and redirect to application view
            conversationmessage = ConversationMessage.objects.create(application=application, content=content, created_by=request.user)
            create_notification(request, application.created_by, "message", extra_id=application.id)
            return redirect('application', application_id=application_id)

        # If content is not provided, treat it as an attempt to edit the application
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('view_application', application_id=application_id)  # Redirect to view application page after editing

    else:
        # If it's a GET request, display the application details and form for editing
        form = ApplicationForm(instance=application)

    return render(request, "userprofile/view_application.html", {"application": application, "form": form})

def edit_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id, created_by=request.user)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated successfully.')
            return redirect('view_application', application_id=application_id)  # Redirect to view application page after editing
    else:
        form = ApplicationForm(instance=application)

    return render(request, "userprofile/edit_application.html", {"form": form, "application": application})


@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, created_by=request.user)
    return render(request, "userprofile/view_task.html", {"task": task})

def approve_application(request, application_id):
    application = Application.objects.get(pk=application_id)
    admin_user = request.user  # Assuming the admin user is the current logged-in user
    assigned_user = application.assigned_to  # Assuming the user to whom the task is assigned
    approved_message = application.approve_and_assign(admin_user, assigned_user)
    
    # Add a success message
    messages.success(request, approved_message)
    
    return redirect('home')  # Redirect to the home page or any other appropriate page
