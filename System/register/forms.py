from django import forms
from .models import User 

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    # Define the choices outside the Meta class
    is_worker_choice = [
        ('False', 'Yes'),
        ('True', 'No')
    ]
    
    is_worker = forms.ChoiceField(choices=is_worker_choice, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'password', 'is_worker']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
