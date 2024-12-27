from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry, Advice
from.forms import EntryForm, AdviceForm
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
            new_entry = form.save()

            mood = new_entry.mood
            print(f"Looking for advice where {mood} is between min_mood and max_mood")
            advices = Advice.objects.filter(min_mood__lte=mood, max_mood__gte=mood)
            print(f"Advice found: {advices}")
            return render(request, 'entries/entry_added.html', {'entry': new_entry, 'advices': advices})
        
    else:
        form = EntryForm()
    
    return render(request, 'entries/add_entry.html', {'form': form})

def advice_list(request):
    advices = Advice.objects.all()
    return render(request, 'entries/advice_list.html', {'advices': advices})

def advice_edit(request, advice_id=None):
    if advice_id:
        advice = get_object_or_404(Advice,id=advice_id)
    else:
        advice = None
    
    if request.method == 'POST':
        form = AdviceForm(request.POST, instance=advice)
        if form.is_valid():
            form.save()
            return redirect('advice_list')
    else:
        form = AdviceForm(instance=advice)

    return render(request, 'entries/advice_edit.html', {'form': form})