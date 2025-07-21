from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#6a11cb')  # Добавлено поле цвета
    
    def __str__(self):
        return self.name

class Note(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новое'),
        ('IN_PROGRESS', 'В процессе'),
        ('DONE', 'Выполнено'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Низкий'),
        ('MEDIUM', 'Средний'),
        ('HIGH', 'Высокий'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    repeat_daily = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.start.strftime('%d.%m.%Y %H:%M')})"