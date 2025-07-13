from django.shortcuts import render, redirect
from .models import Note
from .forms import NoteForm
import calendar
from datetime import date

def index(request):
    today = date.today()
    notes = Note.objects.filter(date=today)
    return render(request, "planner/index.html", {"notes": notes, "today": today})

def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = NoteForm()
    return render(request, "planner/add_note.html", {"form": form})
