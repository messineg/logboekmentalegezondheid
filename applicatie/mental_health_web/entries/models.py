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
    
    def calculate_score(self):
        feedback = self.feedback.aggregate(
            average_score=models.Avg('score'),
            follow_count=models.Count("id", filter=models.Q(followed=True))
        )
        average_score=feedback['average_score'] or 0
        follow_count=feedback['follow_count'] or 0
        return average_score + follow_count
    
class AdviceFeedback(models.Model):

    advice = models.ForeignKey('Advice', on_delete=models.CASCADE, related_name='feedback')
    entry = models.ForeignKey('Entry', on_delete=models.SET_NULL, null=True, blank=True)
    followed = models.BooleanField(default=False)  # Heeft de gebruiker het advies opgevolgd?
    score = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1,11)]) 
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatisch toevoegen tijdstip

    def __str__(self):
        return f"Feedback for advice: {self.advice}"
