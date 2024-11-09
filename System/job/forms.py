from .models import Job
from django import forms

class JobPostForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('repair', 'Repair'),
        ('cleaning_services', 'Cleaning Services'),
        ('massage', 'Massage'),
        ('childcare_services', 'Childcare Services'),
        ('carpentry', 'Carpentry'),
        ('other', 'Other'),  
    ]

    SCHEDULE_CHOICES = [
        ('one_time', 'One-Time'),
        ('fulltime', 'Full-Time'),
        ('parttime', 'Part-Time'),
        ('internship', 'Internship'),
        ('project_work', 'Project Work'),
        ('volunteering', 'Volunteering'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'Gcash'),
        ('credit_debit', 'Credit/Debit'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    schedule = forms.ChoiceField(choices=SCHEDULE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect(attrs={'class': 'form-radio'}))

    class Meta:
        model = Job
        fields = ['title', 'location', 'description', 'date', 'budget', 'payment_method', 'category', 'schedule', 'is_done']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'location': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'budget': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full h-20 border border-gray-300 rounded-md p-2'}),
            'date': forms.DateInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2', 'type': 'date'}),
        }
