from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import  question
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import questionForm
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelformset_factory




from django.shortcuts import render
def questions(request): 
	questions=question.objects.all()
	morequestions=False
	answer=question.objects.filter(user=request.user, answer='')
	number_answer=answer.count()

	if number_answer<3:
		morequestions=True

	if request.method=="POST":
		question_form=questionForm(request.POST)
		if question_form.is_valid():
			content=request.POST.get('content')
			new_question=question.objects.create(user=request.user, content=content)
			new_question.save()
			return redirect('questions')
	else:
		question_form=questionForm()		
	

	context={ 

    'questions':questions,
    'form':question_form,
    'answer':morequestions

	} 

	return render(request, 'question/questions.html',context) 
