from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('add/', views.add_entry, name='add_entry'),
    path('entries/<int:entry_id>/feedback/', views.entry_feedback, name='entry_feedback'),
    path('advice/', views.advice_list, name='advice_list'),
    path('advice/edit/<int:advice_id>/', views.advice_edit, name='advice_edit'),
    path('advice/add', views.advice_edit, name='advice_add'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]