from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('complete/<int:note_id>/', views.complete_note, name='complete_note'),
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/save/', views.calendar_save, name='calendar_save'),
    path('calendar/get/<int:note_id>/', views.calendar_get, name='calendar_get'),
    path('calendar/delete/<int:note_id>/', views.calendar_delete, name='calendar_delete'),
    path('calendar/update_date/<int:note_id>/', views.update_date, name='calendar_update_date'),
]