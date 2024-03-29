# Generated by Django 4.2.7 on 2023-12-21 07:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0011_alter_task_options_task_end_date_task_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='changed_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='task',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorite_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('accepted', 'Accepted'), ('archived', 'Archived'), ('favorite', 'Favorite')], default='active', max_length=20),
        ),
    ]
