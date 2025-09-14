from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=120, unique=True)
    capacity = models.PositiveIntegerField(default=1)
    location = models.CharField(max_length=120, blank=True)
    max_hours = models.PositiveIntegerField(default=4)
    def __str__(self):
        return self.name

class Reservation(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [(PENDING,'pending'),(APPROVED,'approved'),(REJECTED,'rejected')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    note = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return f'{self.room} {self.start_at}'
