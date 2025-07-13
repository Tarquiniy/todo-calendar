from datetime import date

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import NoteForm
from .models import Note

def index(request: HttpRequest) -> HttpResponse:
    """
    Показать задачи на сегодня
    """
    today = date.today()
    notes = Note.objects.filter(date=today)  # ORM-запрос: SELECT * FROM note WHERE date=today
    return render(request, "planner/index.html", {"notes": notes, "today": today})

def add_note(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    """
    Добавить новую задачу
    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = NoteForm()
    return render(request, "planner/add_note.html", {"form": form})
