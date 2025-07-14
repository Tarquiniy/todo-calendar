from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_note, name='add_note'),
    path('edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('complete/<int:note_id>/', views.complete_note, name='complete_note'),
    path('categories/', views.categories, name='categories'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('update_date/<int:note_id>/', views.update_date, name='update_date'),
]
