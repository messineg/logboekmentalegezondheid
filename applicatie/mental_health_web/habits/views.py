# Create your views here.
import datetime
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
from .forms import HabitForm
from .models import Habit, HabitLog

def calendar_view(request):
    today = date.today()
    start_date = today - timedelta(days=today.weekday())
    dates = [start_date + timedelta(days=i) for i in range(7)]

    habits = Habit.objects.filter(user=request.user)
    calendar_data = []

    for habit in habits:
        # Get all logs for the week
        logs = HabitLog.objects.filter(
            habit=habit,
            date__range=(start_date, dates[-1])
        ).select_related('habit')
        
        # Convert logs to dictionary for easy lookup
        logs_dict = {log.date: log for log in logs}

        # Parse days_of_week
        try:
            days_of_week = json.loads(habit.days_of_week) if isinstance(habit.days_of_week, str) else habit.days_of_week or []
        except json.JSONDecodeError:
            days_of_week = []

        days = []
        for current_date in dates:
            day_name = current_date.strftime('%A')
            is_active_day = habit.frequency == 'daily' or (habit.frequency == 'weekly' and day_name in days_of_week)
            log = logs_dict.get(current_date)
            
            days.append({
                'date': current_date,
                'active': is_active_day,
                'completed': log.completed if log else False
            })

        calendar_data.append({
            'habit': habit,
            'days': days
        })

    return render(request, 'habits/calendar.html', {
        'calendar_data': calendar_data,
        'dates': dates,
        'today': today
    })


@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    today_name = today.strftime('%A')

    # Filter for active habits today
    active_habits = habits.filter(
        Q(frequency='daily') |  # All daily habits
        Q(frequency='weekly', days_of_week__icontains=today_name)  # Weekly habits for today
    )
    
    logs_today = HabitLog.objects.filter(
        habit__in=active_habits,
        date=today
    )
    
    completed_today = logs_today.filter(completed=True).count()
    total_active_habits = active_habits.count()
    completion_rate = (completed_today / total_active_habits * 100) if total_active_habits > 0 else 0
    streaks = calculate_streak(request.user)

    context = {
        'habit_data': habits,
        'total_habits': total_active_habits,
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



@require_POST
def toggle_habit(request, habit_id):
    date_str = request.POST.get('date')
    if not date_str:
        return redirect('calendar')
    
    try:
        habit_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        habit = Habit.objects.get(id=habit_id, user=request.user)
        
        log, created = HabitLog.objects.get_or_create(
            habit=habit,
            date=habit_date,
            defaults={'completed': True}
        )
        
        if not created:
            log.completed = not log.completed
            log.save()
            
        return redirect('calendar')
    except (ValueError, Habit.DoesNotExist):
        return redirect('calendar')

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
