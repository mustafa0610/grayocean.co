from .models import question
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class questionForm(forms.ModelForm): 

    content=forms.CharField(widget=forms.TextInput( 

        attrs={ 

            'class':'form-control'  

        } 

    ),label='') 

    class Meta: 

        model=question 

        fields=('content',) 