# Generated by Django 4.2.10 on 2024-04-20 11:37

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Title of task')),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('in_review', 'In Review'), ('done', 'Done')], default='todo', max_length=11)),
                ('due_date', models.DateTimeField(blank=True, null=True, verbose_name='Due date')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date when the task was added')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Completed at')),
                ('assigned_to', models.ManyToManyField(blank=True, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
