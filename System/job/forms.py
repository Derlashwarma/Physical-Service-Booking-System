from .models import Job
from django import forms

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'tag', 'budget', 'description', 'location']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'location': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'budget': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'tag': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }