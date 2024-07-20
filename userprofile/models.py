from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from tasks.models import Application
from django.core.mail import send_mail
from django.conf import settings

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_company = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cell_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    earnings = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    account_type = models.CharField(max_length=10, choices=[('free', 'Free'), ('paid', 'Paid')], default='free')

    def __str__(self):
        return f'{self.user} - {self.email}'

    @property
    def name(self):
        return self.username or self.user.username
    
    @property
    def avatar(self):
        return self.profile_picture.url if self.profile_picture else static('images/avatar.svg')

    @property
    def application_count(self):
        return Application.objects.filter(created_by=self.user).count()

    def add_earnings(self, amount):
        self.earnings += amount
        self.save()

    def request_withdrawal(self, amount):
        if amount <= self.earnings:
            WithdrawalRequest.objects.create(userprofile=self, amount=amount)
            self.earnings -= amount  # Optionally deduct immediately
            self.save()
        else:
            raise ValueError("Insufficient funds for withdrawal.")

User.userprofile = property(lambda u: Userprofile.objects.get_or_create(user=u)[0])


class WithdrawalRequest(models.Model):
    userprofile = models.ForeignKey(Userprofile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userprofile.name} - {self.amount} - {self.status}"

    def notify_user(self):
        subject = "Withdrawal Request Update"
        message = f"Dear {self.userprofile.name},\n\nYour withdrawal request of {self.amount} has been {self.status}.\n\nBest regards,\nYour Company"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.userprofile.email]
        send_mail(subject, message, from_email, recipient_list)

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount earned for this task
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class ConversationMessage(models.Model):
    application = models.ForeignKey(Application, related_name="conversationmessages", on_delete=models.CASCADE)
    content = models.TextField()
    created_by = models.ForeignKey(User, related_name="conversationmessages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
