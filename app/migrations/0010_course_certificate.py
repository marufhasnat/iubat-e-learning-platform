# Generated by Django 4.1.3 on 2022-11-22 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_language_course_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
