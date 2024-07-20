from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from tasks.models import Task, Application, Skill
from django.contrib import messages
from .forms import AddTaskForm, ApplicationForm, TaskSearchForm
from notifications.utilities import create_notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail

# Ensure only admin can access the view
def admin_required(function):
    return user_passes_test(lambda u: u.is_staff)(function)

@admin_required
def approve_and_assign_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    admin_user = request.user  # Current user is the admin approving the application

    try:
        message = application.approve_and_assign(admin_user)
        return render(request, 'tasks/approval_message.html', {'message': message})
    except ValueError as e:
        return render(request, 'tasks/error_message.html', {'error': str(e)})

@login_required
def tasks(request):
    form = TaskSearchForm(request.GET)
    tasks = Task.objects.filter(status=Task.ACTIVE).order_by("-created_at")

    if form.is_valid():
        search_short_description = form.cleaned_data['search_short_description']
        if search_short_description:
            tasks = tasks.filter(short_description__icontains=search_short_description)

    # Pagination setup
    tasks_per_page = 3
    paginator = Paginator(tasks, tasks_per_page)

    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    no_results_message = "No tasks found matching the search criteria." if not tasks else None

    return render(request, "tasks/task.html", {"tasks": tasks, "form": form, "no_results_message": no_results_message})

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    related_tasks = Task.objects.filter(category=task.category).exclude(pk=task_id)[0:3]
    return render(request, "tasks/task_detail.html", {"task": task, "related_tasks": related_tasks})

@login_required
def apply_for_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    skill = Skill.objects.all()

    existing_application = Application.objects.filter(task=task, created_by=request.user).first()
    if existing_application:
        messages.error(request, 'You have already applied for this task.')
        return redirect('profile')

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.task = task
            application.created_by = request.user
            application.save()
            messages.success(request, "You have successfully applied for the task!")
            create_notification(request, task.created_by, "application", extra_id=application.id)
            return redirect('profile')
    else:
        form = ApplicationForm()

    return render(request, "tasks/apply_for_task.html", {"form": form, "task": task, "skill": skill})

def delete_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Application deleted successfully.')
        return redirect('profile')
    
    return render(request, 'tasks/delete_application.html', {'application': application})

@admin_required
def approve_and_assign_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    applications = Application.objects.filter(task=task)

    if request.method == 'POST':
        selected_application_id = request.POST.get('selected_application')
        selected_application = get_object_or_404(Application, pk=selected_application_id)

        # Mark the selected application as approved
        selected_application.approved = True
        selected_application.save()

        # Assign the task to the user who submitted the approved application
        task.assigned_to = selected_application.created_by
        task.assigned = True  # Mark the task as assigned
        task.save()

        # Notify the user about the approval and update earnings
        selected_application.created_by.userprofile.earnings += task.amount  # Add task amount to user's earnings
        selected_application.created_by.userprofile.save()

        return redirect('task_detail', task_id=task_id)

    return render(request, 'tasks/approve_and_assign_task.html', {'task': task, 'applications': applications})

@login_required
def add_task(request):
    if request.method == "POST":
        form = AddTaskForm(request.POST, request.FILES)

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()

            return redirect('profile')
    else:
        form = AddTaskForm()

    return render(request, "tasks/add_task.html", {"form": form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user != task.created_by:
        return render(request, 'view_task.html', {'task': task})

    if request.method == 'POST':
        form = AddTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = AddTaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

@login_required
def archive_or_favorite_page(request, status):
    if status not in [choice[0] for choice in Task.CHOICES_STATUS]:
        return render(request, 'error_page.html', {'message': 'Invalid status'})

    if status == Task.FAVORITE and request.user.is_authenticated:
        tasks = request.user.favorite_tasks.all().order_by('-created_at')
    else:
        tasks = Task.objects.filter(status=status).order_by('-created_at')

    context = {
        'tasks': tasks,
        'status': status,
    }

    return render(request, 'tasks/archive_or_favorite_page.html', context)

@login_required
def toggle_favorite(request, task_id):
    if request.user.is_authenticated:
        task = Task.objects.get(pk=task_id)

        if task in request.user.favorite_tasks.all():
            request.user.favorite_tasks.remove(task)
        else:
            request.user.favorite_tasks.add(task)

    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user == task.created_by:
        task.delete()
        return redirect('profile')
    else:
        return render(request, "tasks/unauthorized_delete.html")

def send_approval_notification(application):
    subject = f"Your application for Task {application.task} has been approved!"
    message = f"Dear {application.created_by.username},\n\n" \
              f"We are pleased to inform you that your application for Task {application.task} has been approved!\n\n" \
              f"You have been assigned to complete this task. Please proceed accordingly.\n\n" \
              f"Thank you,\nYour Organization"

    send_mail(subject, message, 'your_organization@example.com', [application.created_by.email])

def send_approval_notification_view(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    send_approval_notification(application)
    return HttpResponse("Approval notification sent successfully!")
