from django.db import models

class Note(models.Model):  # Модель = таблица в БД
    title = models.CharField(max_length=255)  # заголовок
    content = models.TextField(blank=True)    # текст заметки (может быть пустым)
    date = models.DateField()                # дата, к которой привязана заметка
    created_at = models.DateTimeField(auto_now_add=True)  # когда создана запись

    def __str__(self):
        return f"{self.title} ({self.date})"
