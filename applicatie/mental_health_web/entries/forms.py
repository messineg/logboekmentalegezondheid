from django import forms
from .models import Entry
from django.utils import timezone

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'mood', 'note']  # Velden om in het formulier weer te geven
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'mood': forms.TextInput(attrs={'class': 'input'}),
            'note': forms.Textarea(attrs={'class': 'textarea'}),
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