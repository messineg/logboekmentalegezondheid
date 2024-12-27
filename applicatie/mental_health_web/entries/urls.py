from django.urls import path
from . import views

urlpatterns = [
    path('', views.entry_list, name='entry_list'),
    path('add/', views.add_entry, name='add_entry'),
    path('advice/', views.advice_list, name='advice_list'),
    path('advice/edit/<int:advice_id>/', views.advice_edit, name='advice_edit'),
    path('advice/add', views.advice_edit, name='advice_add'),
]