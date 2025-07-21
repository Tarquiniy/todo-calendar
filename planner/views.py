import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Note, Category
from .forms import NoteForm, CategoryForm
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

def index(request):
    """
    Главная страница со списком задач.
    Фильтрация по статусу, категории, поисковый запрос.
    Также отображается статистика: сколько выполнено.
    """
    notes = Note.objects.all().order_by('start')
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
        'progress_percentage': round((done_count / total_count) * 100) if total_count > 0 else 0,
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

def add_category(request):
    """
    Создание новой категории.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
    return render(request, 'planner/category_form.html', {'form': form, 'title': 'Создать категорию'})


def edit_category(request, category_id):
    """
    Редактирование существующей категории.
    """
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'planner/category_form.html', {'form': form, 'title': 'Редактировать категорию'})

def delete_category(request, category_id):
    """
    Удаление категории.
    """
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('categories')


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
                'start': str(note.start),
                'url': f"/edit/{note.id}/"
            })
        return JsonResponse(events, safe=False)

    return render(request, 'planner/calendar.html', {'categories': Category.objects.all()})

@csrf_exempt
def update_date(request, note_id):
    """
    AJAX‑эндпоинт для обновления даты задачи (drag&drop в календаре).
    """
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)
        try:
            data = json.loads(request.body)
            note.start = datetime.fromisoformat(data['start'])
            if 'end' in data and data['end']:
                note.end = datetime.fromisoformat(data['end'])
            note.save()
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponseBadRequest('Invalid request')

@csrf_exempt
def calendar_events(request):
    events = []
    today = timezone.now().date()
    end_date = today + timedelta(days=365)

    # Получаем все категории сразу для оптимизации
    categories = Category.objects.all()
    category_colors = {cat.id: cat.color for cat in categories}
    category_names = {cat.id: cat.name for cat in categories}

    for note in Note.objects.select_related('category'):
        if note.repeat_daily:
            current_date = note.start.date()
            while current_date <= end_date:
                event_start = timezone.make_aware(
                    datetime.combine(current_date, note.start.time())
                )
                event_end = None
                if note.end:
                    event_end = timezone.make_aware(
                        datetime.combine(current_date, note.end.time())
                    )

                events.append({
                    'id': note.id,
                    'title': note.title,
                    'start': event_start.isoformat(),
                    'end': event_end.isoformat() if event_end else None,
                    'status': note.status,
                    'repeat_daily': note.repeat_daily,
                    'category': note.category.id if note.category else None,
                    'category_name': category_names.get(note.category.id) if note.category else None,
                    'color': category_colors.get(note.category.id) if note.category else None,
                    'content': note.content
                })
                current_date += timedelta(days=1)
        else:
            events.append({
                'id': note.id,
                'title': note.title,
                'start': note.start.isoformat(),
                'end': note.end.isoformat() if note.end else None,
                'status': note.status,
                'repeat_daily': note.repeat_daily,
                'category': note.category.id if note.category else None,
                'category_name': category_names.get(note.category.id) if note.category else None,
                'color': category_colors.get(note.category.id) if note.category else None,
                'content': note.content
            })

    return JsonResponse(events, safe=False, json_dumps_params={'ensure_ascii': False})

@csrf_exempt
def calendar_save(request):
    if request.method == 'POST':
        data = request.POST
        note_id = data.get('noteId')
        title = data.get('title')
        start = data.get('start')
        end = data.get('end')
        content = data.get('content', '')
        status = data.get('status', 'NEW')
        category_id = data.get('category')
        repeat_daily = data.get('repeat_daily') == 'on'

        try:
            if note_id:
                note = Note.objects.get(id=note_id)
            else:
                note = Note()

            note.title = title
            note.content = content
            note.status = status
            note.repeat_daily = repeat_daily

            # Преобразование дат
            note.start = datetime.fromisoformat(start)
            if end:
                note.end = datetime.fromisoformat(end)

            if category_id:
                note.category = Category.objects.get(id=category_id)
            else:
                note.category = None

            note.save()
            return JsonResponse({'status': 'ok', 'id': note.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return HttpResponseBadRequest('Invalid request')

@csrf_exempt
def calendar_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return JsonResponse({'status': 'ok'})

def calendar_get(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return JsonResponse({
        'id': note.id,
        'title': note.title,
        'start': note.start.isoformat(),
        'end': note.end.isoformat() if note.end else None,
        'content': note.content,
        'status': note.status,
        'repeat_daily': note.repeat_daily,
        'category': note.category.id if note.category else None
    })