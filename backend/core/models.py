from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CodingProblem(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    
    def __str__(self):
        return self.title

class UserSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(CodingProblem, on_delete=models.CASCADE)
    code = models.TextField()
    feedback = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} ({self.submitted_at.strftime('%Y-%m-%d %H:%M')})"
