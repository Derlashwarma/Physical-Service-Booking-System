from .models import Job
from django import forms

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'job_type', 'budget', 'description', 'location']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'location': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'budget': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'job_type': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }