from django.shortcuts import render, redirect
from .models import Entry
from.forms import EntryForm
# Create your views here.

def entry_list(request):
    sort = request.GET.get('sort', 'date')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    mood = request.GET.get('mood')


    entries = Entry.objects.all()
    if start_date:
        entries = entries.filter(date__gte=start_date)
    if end_date:
        entries = entries.filter(date__lte=end_date)
    if mood:
        entries = entries.filter(mood=mood)

    if sort in ['date','-date', 'mood', '-mood']:
        entries = entries.order_by(sort)
    return render(request, 'entries/entry_list.html', {'entries': entries})


def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        print("Form is valid: ", form.is_valid())

        if form.is_valid():
            form.save()
            print("Redirecting to entry_list")
            return redirect('entry_list')
        else:
            print("Rendering form with errors")
            return render(request, 'entries/add_entry.html', {'form': form})
    else:
        print("Rendering empty form")
        form = EntryForm()
        return render(request, 'entries/add_entry.html', {'form': form})
