from django import forms
from .models import Habit

DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

class HabitForm(forms.ModelForm):
    
    days_of_week = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Days of the week'
    )
    
    class Meta:
        model = Habit
        fields = ['name', 'description', 'frequency', 'days_of_week', 'category', 'moment_of_day']


class CategoryForm(forms.Form):
    
    class Meta:
        model = Habit
        fields = ['name']