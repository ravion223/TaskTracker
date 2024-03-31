from django import forms
from .models import Task

class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'due_date'
        ]

        labels = {
            'title': '',
            'description': '',
            'status': '',
            'priority': '',
            'due_date': ''
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Task's title"}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Description's title"}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select due date', 'type': 'date'}),
        }


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'status',
            'priority',
            'due_date'
        ]

        labels = {
            'title': '',
            'description': '',
            'status': '',
            'priority': '',
            'due_date': ''
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Task's title"}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Description's title"}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select due date', 'type': 'date'}),
        }