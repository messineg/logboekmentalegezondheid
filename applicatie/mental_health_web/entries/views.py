from django.shortcuts import render
from .models import Entry
# Create your views here.
def entry_list(request):
    entries = Entry.objects.all()
    return render(request, 'entries/entry_list.html', {'entries': entries})