from django import forms
from .models import Note, Category

class NoteForm(forms.ModelForm):
    start = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    end = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'start', 'end', 'status', 'priority',
                 'category', 'repeat_daily', 'attachment']
        widgets = {
            'status': forms.Select(choices=Note.STATUS_CHOICES),
            'priority': forms.Select(choices=Note.PRIORITY_CHOICES),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'color']  