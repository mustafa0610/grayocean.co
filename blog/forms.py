from .models import comment,PostImages,Blog
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
	content=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':'form-control' 
		}
	),label='')
	class Meta:
		model=comment
		fields=('content',)








class CommentSmallForm(forms.ModelForm):
	content=forms.CharField(widget=forms.TextInput(
		attrs={
			'class':'form-control col-5'
		}
	),label='')
	class Meta:
		model=comment
		fields=('content',)


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class PostCreateForm(forms.ModelForm):
	title=forms.CharField(max_length=100)
	content=forms.CharField(widget=forms.Textarea,required=False)

	

	class Meta:
		model=Blog
		fields=('title','content',)
















