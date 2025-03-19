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
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    frequency = models.CharField(
        max_length=10,
        choices=FRECQUENCY_CHOICES,
        default=DAILY,
    )
    days_of_week = models.JSONField(default=list,blank=True)
    moment_of_day = models.CharField(max_length=15, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('evening', 'Evening')], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    exempted_dates = models.JSONField(default=list, blank=True)
    
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

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name