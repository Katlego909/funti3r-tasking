from django.db import models
from django.contrib.auth.models import User
from tasks.models import Application

class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    is_company = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cell_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    earnings = models.DecimalField(default=0, max_digits=10, decimal_places=2)  # Add the earnings field

    def __str__(self):
        return f'{self.user} - {self.email}'

    @property
    def application_count(self):
        return Application.objects.filter(created_by=self.user).count()

User.userprofile = property(lambda u: Userprofile.objects.get_or_create(user=u)[0])

class ConversationMessage(models.Model):
    application = models.ForeignKey(Application, related_name="conversationmessages", on_delete=models.CASCADE)
    content = models.TextField()

    created_by = models.ForeignKey(User, related_name="conversationmessages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
    