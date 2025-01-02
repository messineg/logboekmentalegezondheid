from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Habit(models.Model):

    DAILY = 'daily'
    WEEKLY = 'weekly'
    FRECQUENCY_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    frequency = models.CharField(
        max_length=10,
        choices=FRECQUENCY_CHOICES,
        default=DAILY,
    )
    days_of_week = models.JSONField(default=list,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()
    completed = models.BooleanField(default=False)
    note = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.date} - {self.habit.name}"
    
    class Meta:
        unique_together = ['habit', 'date']