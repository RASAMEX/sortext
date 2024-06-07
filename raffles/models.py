from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Raffle(models.Model):
    """Model representing a raffle."""
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String representation of the Raffle model."""
        return self.name

class Participant(models.Model):
    """Model representing a participant in a raffle."""
    raffle = models.ForeignKey(Raffle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    valid_tickets = models.PositiveIntegerField(default=0)
    invalid_tickets = models.PositiveIntegerField(default=0)

    STATUS_CHOICES = [
        ('Participating', 'Participating'),
        ('Disqualified', 'Disqualified'),
        # Add more statuses if necessary
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Participating')

    def __str__(self):
        """String representation of the Participant model."""
        return f"{self.name} - Raffle: {self.raffle.name}"
