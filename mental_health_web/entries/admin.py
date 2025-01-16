from django.contrib import admin
from .models import Entry, Advice, AdviceFeedback, Emotion, SleepQuality, HealthyActivity, Hobby, Meals, SocialActivity, Weather, PersonalGrowth, Productivity, HouseholdTask
# Register your models here.

admin.site.register(Entry)
admin.site.register(Advice)
admin.site.register(AdviceFeedback)
admin.site.register(Emotion)
admin.site.register(SleepQuality)
admin.site.register(HealthyActivity)
admin.site.register(Hobby)
admin.site.register(Meals)
admin.site.register(SocialActivity)
admin.site.register(Weather)
admin.site.register(PersonalGrowth)
admin.site.register(Productivity)
admin.site.register(HouseholdTask)