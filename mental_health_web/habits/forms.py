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


class ExemptionDateForm(forms.ModelForm):
    exemption_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select a date to exempt this habit'
    )

    class Meta:
        model = Habit
        fields = []  # No model fields, as we're using a custom field

   
    
    def save(self, commit=True):
        habit = super().save(commit=False)
        exemption_date = self.cleaned_data['exemption_date']
    
        # Convert date to string before storing
        exemption_date_str = exemption_date.isoformat()
    
        if habit.exempted_dates is None:
            habit.exempted_dates = []
    
        if exemption_date_str not in habit.exempted_dates:
            habit.exempted_dates.append(exemption_date_str)
    
        if commit:
            habit.save()
        return habit