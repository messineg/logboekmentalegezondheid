from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'mood', 'note']  # Velden om in het formulier weer te geven
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input'}),
            'mood': forms.TextInput(attrs={'class': 'input'}),
            'note': forms.Textarea(attrs={'class': 'textarea'}),
        }
