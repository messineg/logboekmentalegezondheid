from django import forms
from .models import Entry, Advice, AdviceFeedback
from django.utils import timezone

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'mood', 'note', 'emotions', 'sleep_quality', 'healthy_activities', 'hobbies', 'meals', 'social_activities', 'weather', 'personal_growth', 'productivity', 'household_tasks']  # Velden om in het formulier weer te geven
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'mood': forms.TextInput(attrs={'class': 'input'}),
            'note': forms.Textarea(attrs={'class': 'textarea'}),
            'emotions': forms.CheckboxSelectMultiple(),
            'sleep_quality': forms.CheckboxSelectMultiple(),
            'healthy_activities': forms.CheckboxSelectMultiple(),
            'hobbies': forms.CheckboxSelectMultiple(),
            'meals': forms.CheckboxSelectMultiple(),
            'social_activities': forms.CheckboxSelectMultiple(),
            'weather': forms.CheckboxSelectMultiple(),
            'personal_growth': forms.CheckboxSelectMultiple(),
            'productivity': forms.CheckboxSelectMultiple(),
            'household_tasks': forms.CheckboxSelectMultiple(),
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future")
        return date
    
    def clean_mood(self):
        mood = self.cleaned_data['mood']
        if mood < 1 or mood > 10:
            raise forms.ValidationError("Mood must be between 1 and 10")
        return mood
    
class AdviceForm(forms.ModelForm):
    class Meta:
        model = Advice
        fields = ['min_mood', 'max_mood', 'advice']


class AdviceFeedbackForm(forms.ModelForm):
    class Meta:
        model = AdviceFeedback
        fields = ['followed', 'score']