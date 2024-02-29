from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from tasks.models import Task, Application, Category
from userprofile.models import Userprofile
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views import View
from .forms import TicketForm
from django.contrib import messages

def home(request):
    tasks = Task.objects.all()
    categories = Category.objects.all()[0:8]

    # Filtering by category
    if 'category' in request.GET:
        category_id = request.GET['category']
        tasks = tasks.filter(category__id=category_id)

    # Searching by short description
    if 'search' in request.GET:
        search_query = request.GET['search']
        tasks = tasks.filter(short_description__icontains=search_query)

    # Limiting to the first 6 tasks
    tasks = tasks[:6]

    return render(request, "myapp/home.html", {"tasks": tasks, "categories": categories})

def category_tasks(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    tasks = Task.objects.filter(category=category)

    return render(request, "myapp/category_tasks.html", {"category": category, "categories": categories ,"tasks": tasks})

def categories(request):
    categories = Category.objects.all()
    return render(request, "myapp/categories.html", {"categories": categories})

@login_required
def dashboard(request):
    # Get the user profile
    user_profile = Userprofile.objects.get(user=request.user)

    # Render the dashboard template with user_profile and latest_application
    return render(request, "myapp/dashboard.html", {'user_profile': user_profile})

def assign_amount_to_user(application):
    if application.created_by == application.task.assigned_to:
        user_profile = application.task.assigned_to.userprofile
        amount = application.task.amount
        user_profile.earnings += amount
        user_profile.save()

def approve_application(request, application_id):
    application = get_object_or_404(Application, pk=application_id)

    # Assuming approval logic sets application.approved to True
    application.approved = True
    application.save()

    # Check if the application is assigned to a user
    if application.assigned:
        assign_amount_to_user(application)

    # Redirect to dashboard
    return redirect('dashboard')

@login_required
def marketplace (request):
    return render(request, "myapp/marketplace.html", {})

@login_required
def academy (request):
    return render(request, "myapp/academy.html", {} )

@login_required
def task_planner (request):
    return render(request, "myapp/task_planner.html")

@login_required
def recent (request):
    return render(request, "myapp/recent.html", {})

@login_required
def documents (request):
    return render(request, "myapp/documents.html", {})

@login_required
def chatpdf (request):
    return render(request, "myapp/chatpdf.html", {})

@login_required
def assistant (request):
    return render(request, "myapp/assistant.html", {})

@login_required
def account (request):
    return render(request, "myapp/account.html", {})

@login_required
def pricing (request):
    return render(request, "myapp/pricing.html", {})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_created')
    else:
        form = TicketForm()
    return render(request, 'myapp/ticket_form.html', {'form': form})

def ticket_created(request):
    return render(request, 'myapp/ticket_created.html')

def kanban_board(request):
    return render(request, 'myapp/kanban_board.html')

def notes(request):
    return render(request, 'myapp/notes.html')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Use the custom form

        if form.is_valid():  # Correct the condition, it should be form.is_valid() instead of form.is_valid
            user = form.save()

            account_type = request.POST.get("account_type", "agent")

            if account_type == 'company':
                userprofile = Userprofile.objects.create(user=user, is_company=True)
                userprofile.save()
            else:
                userprofile = Userprofile.objects.create(user=user)
                userprofile.save()

            login(request, user)

            return redirect("login")
    else:
        form = CustomUserCreationForm()  # Use the custom form

    return render(request, "myapp/signup.html", {"form": form})

class VerifyEmailView(View):
    def get(self, request, token):
        User = get_user_model()
        user = get_object_or_404(User, verification_token=token)
        user.is_active = True  # Activate the user upon email verification
        user.save()
        return render(request, "myapp/verification_success.html")  # Render a template indicating successful verification


