# Generated by Django 4.2.7 on 2023-12-12 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_alter_task_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='attached_file',
            field=models.FileField(blank=True, null=True, upload_to='task_files/'),
        ),
        migrations.AlterField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='task_images/'),
        ),
    ]