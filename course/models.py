from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True ,null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Course(models.Model):
    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    DURATION_CHOICES = [
        ('1 Week', '1 Week'),
        ('2 Weeks', '2 Weeks'),
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months'),
        ('3 Months', '3 Months'),
        ('6 Months', '6 Months'),
        ('1 Year', '1 Year'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='course_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Beginner')
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, default='1 Week')

    def __str__(self):
        return f"{self.title} - {self.experience_level} | {self.category}"

    def get_lessons(self):
        return self.lessons.all()

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    order = models.PositiveIntegerField()
    content = RichTextField()
    image = models.ImageField(upload_to='lesson_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.course}"

    def get_resources(self):
        return self.resources.all()
    
class Chapter(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField()
    content = RichTextField()

    def __str__(self):
        return self.title

class Resource(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='resource', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='resources/')

    def __str__(self):
        return self.title

class LessonResource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_file = models.FileField(upload_to='lesson_resources/')

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.enrolled_at}"
    
class Progress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Progress'

    def __str__(self):
        return f"{self.student.username} - {self.course.title} - {self.lesson.title}"


