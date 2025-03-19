from django.urls import path
from . import views

urlpatterns = [
    path('', views.habit_list, name='habit_list'),
    path('add/', views.add_habit, name='add_habit'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('toggle-habit/<int:habit_id>/', views.toggle_habit, name='toggle_habit'),
    path('manage/', views.manage_habits, name='manage_habits'),
    path('edit/<int:habit_id>/', views.edit_habit, name='edit_habit'),
    path('categories/manage/', views.manage_categories, name='manage_categories'),
    path('categories/edit/<int:category_id>', views.edit_category, name='edit_category'),
    path('habit/<int:habit_id>/add-exemption/', views.add_exemption_date, name='add_exemption_date'),
]