# Create your views here.
import datetime
from datetime import date, timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Func, Value
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
import json
from .forms import HabitForm, CategoryForm
from .models import Habit, HabitLog, Category
from collections import defaultdict

@login_required
def calendar_view(request):
    today = date.today()
    
    week_offset = int(request.GET.get('week_offset', 0))
    
    start_date = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)

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
        'today': today,
        'week_offset': week_offset
    })


# SQLite gebruikt json_extract om JSON-velden te lezen
class JsonExtract(Func):
    function = "json_extract"
    template = "%(function)s(%(expressions)s)"

@login_required
def habit_list(request):
    print(f"Gebruiker: {request.user}")
    habits = Habit.objects.filter(user=request.user)
    print(f"Habits gevonden: {habits.count()}")
    today = timezone.now().date()
    today_name = today.strftime('%A')

    # Haal alle weekly habits en filter ze in Python
    weekly_habits = [habit for habit in habits if habit.frequency == 'weekly' and today_name in habit.days_of_week]

    active_habits = list(habits.filter(frequency='daily')) + weekly_habits

    logs_today = HabitLog.objects.filter(habit__in=active_habits, date=today)
    adherence_data = {habit.name: calculate_adherence(habit) for habit in active_habits}

    habits_today = [
        {
            'name': habit.name,
            'completed': logs_today.filter(habit=habit, completed=True).exists()
        }
        for habit in active_habits
    ]

    completed_today = logs_today.filter(completed=True).count()
    total_active_habits = len(active_habits)  # Changed this line
    completion_rate = (completed_today / total_active_habits * 100) if total_active_habits > 0 else 0
    streaks = calculate_streak(request.user)

    context = {
        'habit_data': habits,
        'total_habits': total_active_habits,
        'completion_rate': int(completion_rate),
        'streaks': streaks,
        'habits_today': habits_today,
        'adherence': adherence_data
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
@login_required
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


def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('manage_habits')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'habits/edit_category.html', {'form': form, 'title': "Edit Category"})

def manage_categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'habits/manage_categories.html', {'categories': categories})

def calculate_streak(user):
    habits = Habit.objects.filter(user=user)

    streaks = {}

    for habit in habits:
        # Verkrijg de logboeken voor de gewoonte en sorteer op datum
        habit_logs = HabitLog.objects.filter(habit=habit, completed=True).order_by('date')
        
        current_streak = 0
        longest_streak = 0
        previous_log = None

        for log in habit_logs:
            if previous_log and log.date == previous_log.date + timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1  # Reset streak als er een onderbreking is

            longest_streak = max(longest_streak, current_streak)
            previous_log = log

        streaks[habit.name] = {
            'current_streak': current_streak,
            'longest_streak': longest_streak
        }

    return streaks

def calculate_adherence(habit):
    today = date.today()
    start_date = habit.created_at.date()

    # If habit was created today or in the future
    if start_date > today:
        return {'planned_days': 0, 'completed_days': 0, 'adherence_percentage': 0}

    if habit.frequency == 'daily':
        # Calculate all days from creation to today
        planned_days = (today - start_date).days + 1

    elif habit.frequency == 'weekly':
        try:
            days_of_week = json.loads(habit.days_of_week) if isinstance(habit.days_of_week, str) else habit.days_of_week or []
        except json.JSONDecodeError:
            days_of_week = []

        if not days_of_week:
            return {'planned_days': 0, 'completed_days': 0, 'adherence_percentage': 0}

        # Count actual planned days by iterating through each day
        planned_days = 0
        current_date = start_date
        while current_date <= today:
            if current_date.strftime('%A') in days_of_week:
                planned_days += 1
            current_date += timedelta(days=1)

    else:
        return {'planned_days': 0, 'completed_days': 0, 'adherence_percentage': 0}

    # Get completed days
    completed_days = HabitLog.objects.filter(
        habit=habit,
        date__gte=start_date,
        date__lte=today,
        completed=True
    ).count()

    # Calculate adherence
    if planned_days == 0:
        adherence_percentage = 0
    else:
        adherence_percentage = round((completed_days / planned_days) * 100, 2)

    return {
        'planned_days': planned_days,
        'completed_days': completed_days,
        'adherence_percentage': adherence_percentage
    }