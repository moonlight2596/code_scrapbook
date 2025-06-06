from django.db import models

# Create your models here.
from django.conf import settings

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        'auth.User',
        on_dlete=models.CASCADE,
        related_name='projects'
    )
    snippets = models.ManyToManyField(
        'your_app.Snippet',
        related_name='projects'
    )

    primary_editor = models.ForeignKey(
        'snippets.Editor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title