from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Category

class Category(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

# Skills

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Task

class Task(models.Model):
    SIZE_1_9 = "size_1_9"
    SIZE_10_49 = "size_10_49"
    SIZE_50_99 = "size_50_99"
    SIZE_100 = "size_100"

    CHOICES_SIZE = (
        (SIZE_1_9, "1-9"),
        (SIZE_10_49, "10-49"),
        (SIZE_50_99, "50-99"),
        (SIZE_100, "100+"),
    )

    ACTIVE = "active"
    ACCEPTED = "accepted"
    ARCHIVED = "archived"
    FAVORITE = "favorite"

    CHOICES_STATUS = (
        (ACTIVE, "Active"),
        (ACCEPTED, "Accepted"),
        (ARCHIVED, "Archived"),
        (FAVORITE, "Favorite"),
    )

    ENTRY_LEVEL = "entry"
    MID_LEVEL = "mid"
    SENIOR_LEVEL = "senior"

    CHOICES_EXPERIENCE = (
        (ENTRY_LEVEL, "Entry Level"),
        (MID_LEVEL, "Mid Level"),
        (SENIOR_LEVEL, "Senior Level"),
    )

    title = models.CharField(max_length=255)
    short_description = models.TextField()
    long_description = models.TextField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='task_images/', null=True, blank=True)
    attached_file = models.FileField(upload_to='task_files/', null=True, blank=True)

    company_name = models.CharField(max_length=255)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    company_zipcode = models.CharField(max_length=255, blank=True, null=True)
    company_location = models.CharField(max_length=255, blank=True, null=True)
    company_country = models.CharField(max_length=255, blank=True, null=True)
    company_size = models.CharField(max_length=20, choices=CHOICES_SIZE, default=SIZE_1_9)
    company_website = models.URLField(max_length=200, default='https://example.com')
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)

    category = models.ForeignKey(Category, related_name="tasks", on_delete=models.CASCADE)
    
    assigned = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, related_name="assigned_tasks", null=True, blank=True, on_delete=models.SET_NULL)

    skills = models.ManyToManyField(Skill, related_name='tasks', blank=True)  # ManyToMany relationship with Skill

    def is_assigned(self):
        return self.assigned
    
    created_by = models.ForeignKey(User, related_name="tasks", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS, default=ACTIVE)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    experience = models.CharField(max_length=20, choices=CHOICES_EXPERIENCE, default=ENTRY_LEVEL) 

    favorites = models.ManyToManyField(User, related_name='favorite_tasks', blank=True)

    @property
    def countdown_duration(self):
        if self.start_date and self.end_date:
            now = timezone.now()
            time_difference = self.end_date - now

            if now < self.start_date:
                return f"Starts in {time_difference.days} days"
            elif self.start_date <= now <= self.end_date:
                return f"{time_difference.days} days, {time_difference.seconds // 3600} hours, {time_difference.seconds % 3600 // 60} minutes"
            else:
                return "Task has ended and closed"
        else:
            return "Start date or end date not set"

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

# Application

class Application(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    APPROVAL_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    task = models.ForeignKey(Task, related_name="applications", on_delete=models.CASCADE)
    cover_letter = models.TextField()
    experience = models.TextField()
    email = models.EmailField(default="")
    resume = models.FileField(upload_to='resumes/', default="")  # Adjust the upload_to path as needed
    linkedin_profile = models.URLField(blank=True, null=True)

    created_by = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(User, related_name="approved_applications", on_delete=models.CASCADE, blank=True, null=True)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default=PENDING)
    assigned_to = models.ForeignKey(User, related_name="assigned_applications", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Application for Task {self.task} by {self.created_by.username} ({self.email})"

    def calculate_task_amount(self):
        return self.task.amount

    def approve_and_assign(self, admin_user, assigned_user):
        """
        Method to approve and assign the application to a user by an admin.
        """
        if self.approval_status == self.PENDING:
            self.approval_status = self.APPROVED
            self.approved_by = admin_user
            self.assigned_to = assigned_user
            self.save()

            # Construct email message
            subject = f"Task Assignment Notification"
            message = f"Your application for Task {self.task} has been approved and assigned to {assigned_user.username}."
            from_email = 'katlego.hlangwane@gmail.com'  # Update with your email address
            to_email = self.email  # Assuming email is the user's email field in the Application model

            # Send email
            send_mail(subject, message, from_email, [to_email])

            return f"Your application for Task {self.task} has been approved and assigned to {assigned_user.username}. An email notification has been sent."
        else:
            raise ValueError("Application is not pending approval.")