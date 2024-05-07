from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Represents a task with properties such as title, description, status, and due date. 
    It supports assignment to multiple users and managing multiple attachments.
    """
    # Status choices for a task
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('in_review', 'In Review'),
        ('done', 'Done'),
    ]

    title = models.CharField(
        "Title of task", max_length=64, help_text="Enter a short, descriptive title for the task.")
    description = models.TextField(help_text="Provide a detailed description of the task.")
    status = models.CharField(
        "Current status of task", max_length=11, choices=STATUS_CHOICES, default='todo',
        help_text="Select the current status of the task. Choose from To Do, In Progress, In Review, or Done.")
    assigned_to = models.ManyToManyField(
        User, blank=True, related_name='assigned_tasks',
        help_text="Assign this task to one or more team members.")
    due_date = models.DateTimeField(
        "Due date of task", null=True, blank=True,
        help_text="Optionally set a deadline for when the task needs to be completed.")
    created_at = models.DateTimeField(
        "Creation date of task", default=timezone.now,
        help_text="The date and time the task was created. This is automatically set and should not be changed.")
    completed_at = models.DateTimeField(
        "Completion date of task", null=True, blank=True,
        help_text="The date and time the task was completed. Update this when the task is marked as done.")
    attachment1 = models.FileField(
        "First attachment", upload_to="task_attachments/", blank=True, null=True,
        help_text="Upload a relevant file as the first attachment for this task.")
    attachment2 = models.FileField(
        "Second attachment", upload_to="task_attachments/", blank=True, null=True,
        help_text="Upload a relevant file as the second attachment for this task.")
    attachment3 = models.FileField(
        "Third attachment", upload_to="task_attachments/", blank=True, null=True,
        help_text="Upload a relevant file as the third attachment for this task.")

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"

class TaskComment(models.Model):
    """
    Represents a comment on a task, with the ability to manage multiple attachments.
    """
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_comments',
        help_text="The user who created this comment.")
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments',
        help_text="The task this comment is associated with.")
    comment = models.TextField(help_text="The text content of the comment.")
    created_at = models.DateTimeField(
        "Creation date of comment", auto_now_add=True,
        help_text="The date and time this comment was created. Automatically set at the time of creation.")
    attachment = models.FileField(
        "First attachment for comment", upload_to="comment_attachments/", blank=True, null=True,
        help_text="Upload a file related to this comment, if necessary.")
    attachment2 = models.FileField(
        "Second attachment for comment", upload_to="comment_attachments/", blank=True, null=True,
        help_text="Optionally add a second file attachment related to this comment.")
    attachment3 = models.FileField(
        "Third attachment for comment", upload_to="comment_attachments/", blank=True, null=True,
        help_text="Optionally add a third file attachment related to this comment.")

    def __str__(self):
        return f"Comment by {self.creator.username} on {self.task.title}"
