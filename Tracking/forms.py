from django import forms
from .models import Task, Comment, Profile

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


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name_surname',
            'bio',
            'email',
            'profile_pic'
        ]
        labels = {
            'name_surname' : '',
            'bio': '',
            'email': '',
            'profile_pic': ''
        }
        widgets = {
            'name_surname': forms.TextInput(attrs={'class': 'form-class', 'placeholder': 'Name and surname'}),
            'bio': forms.TextInput(attrs={'class': 'form-class', 'placeholder': 'Bio'}),
            'email': forms.EmailInput(attrs={'class': 'form-class', 'placeholder': 'Email'}),
        }


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All'),
        ('todo', "To Do"),
        ('in_progress', "In progress"),
        ('done', 'Done')
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='status', required=False)


class TaskCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'})
        }