from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Note, Category
from .forms import NoteForm, CategoryForm
from datetime import date
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """
    Главная страница со списком задач.
    Фильтрация по статусу, категории, поисковый запрос.
    Также отображается статистика: сколько выполнено.
    """
    notes = Note.objects.all().order_by('date')
    status = request.GET.get('status')
    category = request.GET.get('category')
    q = request.GET.get('q')

    if status:
        notes = notes.filter(status=status)
    if category:
        notes = notes.filter(category_id=category)
    if q:
        notes = notes.filter(title__icontains=q)

    done_count = Note.objects.filter(status='DONE').count()
    total_count = Note.objects.count()
    categories = Category.objects.all()

    context = {
        'notes': notes,
        'categories': categories,
        'done_count': done_count,
        'total_count': total_count,
    }
    return render(request, 'planner/index.html', context)


def add_note(request):
    """
    Создание новой задачи.
    """
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm()
    return render(request, 'planner/form.html', {'form': form, 'title': 'Новая задача'})


def edit_note(request, note_id):
    """
    Редактирование существующей задачи.
    """
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = NoteForm(instance=note)
    return render(request, 'planner/form.html', {'form': form, 'title': 'Редактировать задачу'})


def delete_note(request, note_id):
    """
    Удаление задачи.
    """
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('index')


def complete_note(request, note_id):
    """
    Отметить задачу как завершённую.
    """
    note = get_object_or_404(Note, id=note_id)
    note.status = 'DONE'
    note.save()
    return redirect('index')


def categories(request):
    """
    Страница категорий: список и форма создания.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()

    categories = Category.objects.all()
    return render(request, 'planner/categories.html', {'form': form, 'categories': categories})


def calendar_view(request):
    """
    Страница календаря с FullCalendar.js.
    Если AJAX — отдаёт JSON событий.
    """
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        events = []
        for note in Note.objects.all():
            events.append({
                'id': note.id,
                'title': note.title,
                'start': str(note.date),
                'url': f"/edit/{note.id}/"
            })
        return JsonResponse(events, safe=False)

    return render(request, 'planner/calendar.html')


@csrf_exempt
def update_date(request, note_id):
    """
    AJAX‑эндпоинт для обновления даты задачи (drag&drop в календаре).
    """
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)
        new_date = request.POST.get('date')
        if new_date:
            note.date = new_date
            note.save()
            return JsonResponse({'status': 'ok'})
    return HttpResponseBadRequest('Invalid request')
