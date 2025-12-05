from django.db import models
from django.contrib.auth.models import User

class Match(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    total_cost = models.IntegerField(default=0)
    organizer_info = models.TextField(blank=True, help_text="Bank details for payment")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_matches', null=True)

    def __str__(self):
        return f"Match at {self.location} on {self.date.strftime('%Y-%m-%d %H:%M')}"

class Attendance(models.Model):
    TEAM_CHOICES = [
        ('WHITE', 'White'),
        ('COLOR', 'Color'),
    ]

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='attendances')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, help_text="Name for guest players")
    is_confirmed = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)
    team = models.CharField(max_length=10, choices=TEAM_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.name or (self.user.username if self.user else "Unknown")

    @property
    def player_name(self):
        return self.name or (self.user.username if self.user else "Unknown")
