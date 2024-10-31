import re
from django import forms
from .models import CustomUser 
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full border border-gray-600 rounded-md'}))
    
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
            'username': forms.TextInput(attrs={'class': 'w-full border border-gray-600 rounded-md'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_pattern = r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[^\d\s]).{5,}$'
        if not re.match(password_pattern, password):
            return self.add_error('password', "Must be at least 5 characters long, one uppercase letter, one number, and one special character")
        return password
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            return self.add_error('username',"A user with that username already exists.")
        return username
    
    def save(self, commit=True, *args, **kwargs):
        user = super().save(commit=False, *args, **kwargs)
        user.password = make_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
        
        return user

class AdminUserForm(forms.ModelForm):
    class Meta:
        model= CustomUser
        fields= '__all__'
        exclude=['password', 'groups', 'user_permissions']