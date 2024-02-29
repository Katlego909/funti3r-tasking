from django.contrib import admin
from .models import  Category, Skill,Task, Application

admin.site.register(Category)
admin.site.register(Skill)
admin.site.register(Task)
admin.site.register(Application)
