from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry, Advice, AdviceFeedback
from.forms import EntryForm, AdviceForm, AdviceFeedbackForm
from django.db.models import Avg, Count, Max, Min, Q, Exists, OuterRef
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def entry_list(request):
    sort = request.GET.get('sort', 'date')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    mood = request.GET.get('mood')

    entries = Entry.objects.annotate(
        has_feedback=Exists(
            AdviceFeedback.objects.filter(entry=OuterRef('pk'))
        )
    )

    if start_date:
        entries = entries.filter(date__gte=start_date)
    if end_date:
        entries = entries.filter(date__lte=end_date)
    if mood:
        entries = entries.filter(mood=mood)

    if sort in ['date','-date', 'mood', '-mood']:
        entries = entries.order_by(sort)
    
    if not sort:
        sort = '-date'

    return render(request, 'entries/entry_list.html', {'entries': entries})


def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        print("Form is valid: ", form.is_valid())

        if form.is_valid():
            new_entry = form.save()
            mood = new_entry.mood
            advices = Advice.objects.filter(min_mood__lte=mood, max_mood__gte=mood)
            sorted_advices = sorted(advices, key=lambda advice: advice.calculate_score(), reverse=True)
            return render(request, 'entries/entry_added.html', {'entry': new_entry, 'advices': sorted_advices})
        
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



def entry_feedback(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    
    # Haal min_mood en max_mood waarden op, stel deze in op een standaard als ze niet bestaan
    min_mood = request.GET.get('min_mood', 0)  # Stel dat dit via de GET request komt
    max_mood = request.GET.get('max_mood', 10)  # Stel dat dit via de GET request komt

    # Haal adviezen op die voldoen aan de min_mood en max_mood voorwaarden
    advices = Advice.objects.filter(min_mood__lte=entry.mood, max_mood__gte=entry.mood)
    

    if request.method == "POST":
        advice_id = request.POST.get("advice_id")
        followed = request.POST.get("followed") == "on"
        score = request.POST.get("score")
        if advice_id and score and score.isdigit():
            advice = get_object_or_404(Advice, id=advice_id)
            AdviceFeedback.objects.create(
                entry=entry,
                advice=advice,
                followed=followed,
                score=int(score)
            )
            return redirect('entry_feedback', entry_id=entry.id)

    return render(request, 'entries/entry_feedback.html', {'entry': entry, 'advices': advices})


def statistics_view(request):
    # Mood statistieken
    avg_mood = Entry.objects.aggregate(Avg('mood'))['mood__avg']
    min_mood = Entry.objects.aggregate(Min('mood'))['mood__min']
    max_mood = Entry.objects.aggregate(Max('mood'))['mood__max']
    total_entries = Entry.objects.count()

    # Advies feedback statistieken
    feedback_stats = AdviceFeedback.objects.aggregate(
        avg_score=Avg('score'),
        total_feedbacks=Count('id'),
        followed_feedbacks=Count('id', filter=Q(followed=True))
    )

    advices = Advice.objects.annotate(
        avg_score=Avg('feedback__score', filter=Q(feedback__score__isnull=False)),
        feedback_count=Count('feedback', filter=Q(feedback__score__isnull=False))
    ).order_by('-avg_score', '-feedback_count')  # Sorteer op gemiddelde score en feedback count

    context = {
        'avg_mood': avg_mood,
        'min_mood': min_mood,
        'max_mood': max_mood,
        'total_entries': total_entries,
        'feedback_stats': feedback_stats,
        'advices': advices,
    }

    return render(request, 'entries/statistics.html', context)



    
