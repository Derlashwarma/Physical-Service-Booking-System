import re
from django import forms
from .models import CustomUser 
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control mx-2'}))
    
    # Define the choices outside the Meta class
    is_worker_choice = [
        ('False', 'Yes'),
        ('True', 'No')
    ]
    
    is_worker = forms.ChoiceField(choices=is_worker_choice, widget=forms.RadioSelect(attrs={
        'class': 'mt-3 flex-right'
    }))

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'is_worker']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mx-2'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_pattern = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[^\d\s]).{5,}$'
        if not re.match(password_pattern, password):
            self.add_error('password', "Must be at least 5 characters long, one uppercase letter, one number, and one special character")
        return password
    
    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False, *args, **kwargs)
        user.password = make_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user
