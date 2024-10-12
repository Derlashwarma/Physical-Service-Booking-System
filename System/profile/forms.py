from django import forms
from register.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','professional_summary', 'professional_experience',
                  'key_skills','social_contacts','image','field_of_work',
                  'previous_employment']
        
        widgets={
            'first_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'professional_summary': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'professional_experience': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'key_skills': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'social_contacts': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'field_of_work': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
            'previous_employment': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-md p-2'}),
        }