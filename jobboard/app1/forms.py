from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Application, Job

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email", widget=forms.EmailInput)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['email', 'first_name', 'last_name', 'cover_letter', 'cv']


#validation for cover letter 
    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        if len(cover_letter) not in range(200, 1024):
            raise forms.ValidationError("cover letter must be in range of 200-1024 characters long.")
        return cover_letter

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['email', 'title', 'location', 'type', 'description', 'company_name', 'company_description', 'logo']

# validation  for description 
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) not in range(200, 1024):
            raise forms.ValidationError("Description must be in range of 200-1024 characters long.")
        return description