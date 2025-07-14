from django import forms
from .models import Note, Category

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'date', 'status', 'priority', 'category', 'repeat_daily', 'attachment']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
