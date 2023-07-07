from django import forms
from .models import CustomUser
from datetime import date
from .models import UploadedFiles
from django.contrib.auth.hashers import make_password

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'fullname', 'dob', 'visibility')

    def save(self, commit=True):
        instance = super().save(commit=False)
        year_of_birth = self.cleaned_data['dob']
        passw = self.cleaned_data['password']
        passw = make_password(passw)
        age = calculate_age(year_of_birth)
        instance.age = age
        instance.password = passw

        if commit:
            instance.save()

        return instance

def calculate_age(year_of_birth):
    current_year = date.today().year
    age = current_year - year_of_birth
    return age

class UploadBookForm(forms.ModelForm):
    class Meta:
        model = UploadedFiles
        fields = ['title', 'description', 'visibility', 'cost', 'year_published', 'file', 'username']
