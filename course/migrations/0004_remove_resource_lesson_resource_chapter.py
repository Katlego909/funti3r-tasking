# Generated by Django 4.2.7 on 2024-02-13 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_resource_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='lesson',
        ),
        migrations.AddField(
            model_name='resource',
            name='chapter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='resource', to='course.chapter'),
            preserve_default=False,
        ),
    ]