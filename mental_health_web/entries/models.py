from django.db import models

# Create your models here.

class Entry(models.Model):
    mood = models.IntegerField()
    date = models.DateField()
    note = models.TextField()

    #many to many relationships
    emotions = models.ManyToManyField('Emotion', blank=True, null=True)
    sleep_quality = models.ManyToManyField('SleepQuality', blank=True, null=True)
    healthy_activities = models.ManyToManyField('HealthyActivity', blank=True, null=True)
    hobbies = models.ManyToManyField('Hobby', blank=True, null=True)
    meals = models.ManyToManyField('Meals', blank=True, null=True)
    social_activities = models.ManyToManyField('SocialActivity', blank=True, null=True)
    weather = models.ManyToManyField('Weather', blank=True, null=True)
    personal_growth = models.ManyToManyField('PersonalGrowth', blank=True, null=True)
    productivity = models.ManyToManyField('Productivity', blank=True, null=True)
    household_tasks = models.ManyToManyField('HouseholdTask', blank=True, null=True)


    def __str__(self):
        return f"{self.date} - Mood: {self.mood} - Note: {self.note}"
    
    class Meta:
        db_table = 'Entries'

class Emotion(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'Emotions'

class SleepQuality(models.Model):
    quality = models.CharField(max_length=255)

    def __str__(self):
        return f"Quality: {self.quality}"
    
    class Meta:
        db_table = 'SleepQuality'

class HealthyActivity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'HealthyActivities'

class Hobby(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'Hobbies'

class Meals(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'Meals'

class SocialActivity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'SocialActivities'

class Weather(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'Weather'


class PersonalGrowth(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'PersonalGrowth'

class Productivity(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'Productivity'

class HouseholdTask(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'HouseholdTasks'

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
    score = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1,6)]) 
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatisch toevoegen tijdstip

    def __str__(self):
        return f"Feedback for advice: {self.advice}"
