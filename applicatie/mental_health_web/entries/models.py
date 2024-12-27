from django.db import models

# Create your models here.

class Entry(models.Model):
    mood = models.IntegerField()
    date = models.DateField()
    note = models.TextField()

    def __str__(self):
        return f"{self.date} - Mood: {self.mood} - Note: {self.note}"
    
    class Meta:
        db_table = 'Entries'

class Advice(models.Model):
    min_mood = models.IntegerField()
    max_mood = models.IntegerField()
    advice = models.TextField()

    def __str__(self):
        return f"{self.advice}"
    