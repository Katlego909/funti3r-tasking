# Generated by Django 4.2.7 on 2024-02-13 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_alter_chapter_content_alter_course_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='experience_level',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=20),
        ),
    ]