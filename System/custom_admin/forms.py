from django import forms
from job.models import JobApplication

class ApplicationForm(forms.ModelForm):
    class Meta:
        model= JobApplication
        fields= '__all__' 