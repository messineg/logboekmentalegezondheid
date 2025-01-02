# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import HabitForm
from datetime import date, timedelta
from django.utils.timezone import now
from .models import Habit, HabitLog
from django.db.models import Count, Q
from datetime import timedelta

@login_required
def calendar_view(request):
    today = date.today()
    start_date = today - timedelta(days=today.weekday())  # Start van de huidige week (maandag)
    dates = [start_date + timedelta(days=i) for i in range(7)]  # Weekdagen

    habits = Habit.objects.filter(user=request.user)
    calendar_data = []

    for habit in habits:
        logs = {log.date: log for log in HabitLog.objects.filter(habit=habit, date__range=(start_date, dates[-1]))}
        days = []
        for day in dates:
            if habit.frequency=='weekly' and day.strftime('%A') not in habit.days_of_week:
                continue

            habit_log = logs.get(day)  # Haal de log op voor deze dag (indien aanwezig)
            completed = habit_log.completed if habit_log else False  # Controleer of de log voltooid is
            days.append({'date': day, 'completed': completed})
        calendar_data.append({'habit': habit, 'days': days})

    return render(request, 'habits/calendar.html', {'calendar_data': calendar_data, 'dates': dates})


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    
    logs_today = HabitLog.objects.filter(habit__user =request.user, date=today)
    completed_today = logs_today.filter(completed=True).count()
    total_habits = habits.count()
    completion_rate = (completed_today / total_habits) * 100 if total_habits > 0 else 0
    streaks = calculate_streak(request.user)

    context = {
        'habit_data': habits,
        'total_habits': total_habits,
        'completion_rate': int(completion_rate),
        'streaks': streaks,
    }

    return render(request, 'habits/habit_list.html', context)

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('manage_habits')
    else:
        form = HabitForm()
    
    return render(request, 'habits/habit_form.html', {'form': form})



def toggle_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = now().date()
    
    # Probeer een bestaande log te vinden
    log, created = HabitLog.objects.get_or_create(habit=habit, date=today)
    
    # Toggle de status
    log.completed = not log.completed
    log.save()
    
    # Redirect naar de vorige pagina (meestal de kalender)
    return redirect(request.META.get('HTTP_REFERER', 'calendar'))

@login_required
def manage_habits(request):
    habits = Habit.objects.filter(user=request.user)

    if request.method == 'POST' and 'delete_habit' in request.POST:
        habit_id = request.POST.getlist('habit_id')
        habits = get_object_or_404(Habit, id=habit_id, user=request.user)
        habits.delete()

        return redirect('manage_habits')

    return render(request, 'habits/manage_habits.html', {'habits': habits})

def edit_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)

    if request.method == 'POST':
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            habit = form.save()
            return redirect('manage_habits')
    else:
        form = HabitForm(instance=habit)
    
    return render(request, 'habits/habit_form.html', {'form': form, 'title': "Edit Habit"})




def calculate_streak(user):
    habits = Habit.objects.filter(user=user)

    streaks = {}

    for habit in habits:
        # Verkrijg de logboeken voor de gewoonte en sorteer op datum
        habit_logs = HabitLog.objects.filter(habit=habit).order_by('-date')
        
        streak = 0
        current_streak = 0
        previous_log = None

        for log in habit_logs:
            if log.completed:
                # Als de vorige log bestaat en de datum is een dag eerder, verhoog de streak
                if previous_log and previous_log.date == log.date - timedelta(days=1):
                    current_streak += 1
                else:
                    # Als er een onderbreking is, begin een nieuwe streak
                    current_streak = 1

                streak = max(streak, current_streak)
            
            previous_log = log

        streaks[habit.name] = streak

    return streaks
