# Generated by Django 4.2.7 on 2024-02-13 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_course_experience_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='duration',
            field=models.CharField(choices=[('1 Week', '1 Week'), ('2 Weeks', '2 Weeks'), ('1 Month', '1 Month'), ('2 Months', '2 Months'), ('3 Months', '3 Months'), ('6 Months', '6 Months'), ('1 Year', '1 Year')], default='1 Week', max_length=20),
        ),
    ]
