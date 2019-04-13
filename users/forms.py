from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=['username','email','password1','password2']




class UserUpdateForm(forms.ModelForm):
	email=forms.EmailField()

	class Meta:
		model=User
		fields=['username','email']	


class ProfileUpdateForm(forms.ModelForm):
	image=forms.ImageField(label='Profile Picture')
	class Meta:
		model=Profile
		fields=['image','description']


class MyLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.placeholder = 'Username'
        self.fields['password'].widget.placeholder = 'Password'