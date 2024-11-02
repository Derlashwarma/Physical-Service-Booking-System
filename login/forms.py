from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget = forms.TextInput(attrs={
        'class': 'rounded-md'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'rounded-md'
    }))