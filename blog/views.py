from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Blog, comment, Report, PostImages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.forms import CommentForm, CommentSmallForm, PostCreateForm
from django.contrib.auth.decorators import login_required
from .forms import PostCreateForm
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















def BlogsList(request):
	search_term=''
	if 'search' in request.GET:
		search_term_extract = request.GET['search']
		search_term = Blog.objects.filter(Q(title__icontains=search_term_extract)|Q(author__username__icontains=search_term_extract))
		paginator = Paginator(search_term, 8)
		page = request.GET.get('page')
		paginator_page = paginator.get_page(page)
		results=search_term.all()
		message=True
		nav=False
	else:
		blogs=None
		paginator =None
		page=None
		paginator_page=None
		search_term_extract=''
		message=False
		nav=True
	context={'blogs':paginator_page,'search_term_extract': search_term_extract,'message':message,'nav':nav}
	return render(request, 'blog/home.html',context)


def about(request):
	return render(request,'blog/about.html')



class UserBlogsList(ListView):
    model = Blog
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Blog.objects.filter(author=user).order_by('-date_posted')
    def user_details(self):
    	user = get_object_or_404(User, username=self.kwargs.get('username'))
    	context=user.profile.description
    	return context



def user_blog_list(self,username):
	blogs=get_object_or_404(klass, blog__author=username)
	context={
	'posts':blogs
	}
	return render(request,'blog/user_posts.html',context)


class CommentList(ListView):
	model=comment
	template_name='blog/comment_list.html'
	context_object_name='comments'
	paginate_by=8




def post_detail(request, pk):
	post=get_object_or_404(Blog, pk=pk)
	comments=comment.objects.filter(post=post).order_by('-id')[:5]
	comment_full=comment.objects.filter(post=post).order_by('-id')
	comment_count=comment.objects.filter(post=post)
	comment_actual_count=comment_count.count()
	there_are_comments=False
	if comment_actual_count > 0:
		there_are_comments=True
	likes=post.likes.count()
	dislikes=post.dislikes.count()
	score=likes-dislikes
	if request.method=="POST":
		comment_form=CommentForm(request.POST)
		if comment_form.is_valid():
			content=request.POST.get('content')
			new_comment=comment.objects.create(post=post, user=request.user, content=content)
			new_comment.save()
			return HttpResponseRedirect(Blog.redirect_route(blog_id=pk))
	else:
		comment_form= CommentForm()




	is_commented=False
	if comment.objects.filter(user=request.user.id,post=post).exists():
		is_commented=True


	context={
		'score':score,
		'there_are_comments':there_are_comments,
		'post':post,
		'is_liked': post.likes.filter(id=request.user.id).exists(),
		'is_disliked': post.dislikes.filter(id=request.user.id).exists(),
		'likes':post.likes,
		'dislikes':post.dislikes,
        'comments':comments,
        'comment_form':comment_form,
        'comment_full':comment_full,
        'is_commented':is_commented
        }
	return render(request, 'blog/post_detail.html',context)




def dislike_post(request, blog_id):
	post = get_object_or_404(Blog, id=blog_id)
	is_liked=False
	is_disliked=False
	if post.dislikes.filter(id=request.user.id).exists():
		post.dislikes.remove(request.user)
		is_disliked=False
	elif post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked=False
		is_disliked=False
	else:
		post.dislikes.add(request.user)
		is_disliked=True
	context={
		'post':post,
		'is_disliked': post.dislikes.filter(id=request.user.id).exists(),
		'is_liked': post.likes.filter(id=request.user.id).exists(),

        }
	return HttpResponseRedirect(Blog.redirect_route(blog_id))

def like_post(request, blog_id):
	post = get_object_or_404(Blog, id=blog_id)
	is_liked=False
	is_disliked=False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked=False
	elif post.dislikes.filter(id=request.user.id).exists():
		post.dislikes.remove(request.user)
		is_liked=False
		is_disliked=False
	else:
		post.likes.add(request.user)
		is_liked=True
	context={
		'post':post,
		'is_liked': post.likes.filter(id=request.user.id).exists(),
		'is_disliked': post.dislikes.filter(id=request.user.id).exists(),
        }
	return HttpResponseRedirect(Blog.redirect_route(blog_id))


def report_post(request, blog_id):
	post = get_object_or_404(Blog, id=blog_id)
	if Report.objects.filter(post=post,user=request.user):
		messages.success(request, f"You've already reported this post, either it hasn't been reviewed yet or it doesn't go against our guidelines.")
	else:
		Report.objects.create(post=post,user=request.user)
		messages.success(request,f'This post has been reported and our team will review it within 48 hours')
	context={
	'post':post
	}
	return HttpResponseRedirect(Blog.redirect_route(blog_id))



@login_required(login_url='/login/')
def profile(request):
	return render(request, 'users/profile.html')

@login_required(login_url='/login/')
def not_creator(request):
	return render(request, 'users/not_creator.html')







# def like_post(request, pk):
# 	post = get_object_or_404(Blog, pk=pk)
# 	is_liked=False
# 	if post.likes.filter(id=request.user.id).exists():
# 		post.likes.remove(request.user)
# 		is_liked=False
# 	else:
# 		post.likes.add(request.user)
# 		is_liked=True
# 	context={
# 		'post':post,
# 		'is_liked': post.likes.filter(id=request.user.id).exists(),
#         }
# 	return HttpResponseRedirect(Blog.get_absolute_url())




# def dispatch(self, *args, **kwargs):


# return super(MyView, self).dispatch(*args, **kwargs)


def check_liked(request):
	post = get_object_or_404(Blog, id=blog_id)
	is_liked=False
	if post.likes.filter(id=request.User.id).exists():
		is_liked=True
	else:
		is_liked=False
	context={
	'is_liked':is_liked
	}
	return render(request, 'blog/post_detail.html',context)


class PostCreateView(LoginRequiredMixin, CreateView):
	@method_decorator(user_passes_test(lambda u: u.is_staff))
	def dispatch(self, *args,**kwargs):
		return super(PostCreateView,self).dispatch(*args,**kwargs)
	model=Blog
	fields=['title','content','image','image1','image2','image3','image4','video']
	login_url = "/login/"
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin ,UpdateView):
	model=Blog
	fields=['title','content','image','image1','image2','image3','image4','video']
	login_url = "/login/"
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)

	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
        	return True
        return False


def comments_list(request, blog_id):
	post=get_object_or_404(Blog, id=blog_id)
	comments=comment.objects.filter(post=post).order_by('-id')
	paginator = Paginator(comments, 8)
	page = request.GET.get('page')
	comments = paginator.get_page(page)
	comments_count=comment.objects.filter(post=post)



	if request.method=="POST":
		comment_form=CommentSmallForm(request.POST)
		if comment_form.is_valid():
			content=request.POST.get('content')
			new_comment=comment.objects.create(post=post, user=request.user, content=content)
			new_comment.save()
			return HttpResponseRedirect(Blog.to_comments(blog_id=blog_id))
	else:
		comment_form= CommentSmallForm()

	context={
		'post':post,
		'is_liked': post.likes.filter(id=request.user.id).exists(),
        'comments':comments,
        'comment_form':comment_form,
        'comments_count':comments_count,
        }
	return render(request, 'blog/comment_list.html',context)







def comment_delete(request, pk):
	comment_to_delete=get_object_or_404(comment,pk=pk)
	if request.method=='POST':
		if comment_to_delete.user == request.user:
			post_url=comment_to_delete.post.id
			comment_to_delete.delete()
			messages.success(request, 'Your comment has been deleted')
			return HttpResponseRedirect('/post/'+str(post_url))

	context={
		'comment':comment_to_delete
	}
	return render(request, 'blog/comment_confirm_delete.html', context)


def comment_detail(request,pk):
	comment_detail=get_object_or_404(comment, pk=pk)
	context={
		'comment':comment_detail
	}
	return render(request, 'blog/comment_detail.html',context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = comment
    success_url = reverse_lazy('post-detail')


    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
        	return True
        return False



# def search_blog_list(request):
#     posts_search = Blog.objects.all()
#     search_term_extract=''
#     blogs=None

#     if 'search' in request.GET:
#         search_term_extract = request.GET['search']
#         search_term = Blog.objects.filter(title__icontains=search_term_extract)
#         blogs=search_term.all()
#         paginator = Paginator(blogs, 2)
#         page = request.GET.get('page')
#         blogs = paginator.get_page(page)






#     get_dict_copy = request.GET.copy()
#     params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

#     context = {'blogs': blogs, 'params': params, 'search_term_extract': search_term_extract}
#     return render(request, 'blog/search_blogs.html', context)


def post_create(request):
	ImageFormset = modelformset_factory(PostImages, fields=('image',), extra=7)
	if request.method=='POST':
		form=PostCreateForm(request.POST)
		formset=ImageFormset(request.POST or None, request.FILES or None)
		if form.is_valid() and formset.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			pk=post.id

			for f in formset.cleaned_data:
				try:
					photo=PostImages.objects.create(post=post,image=f['image'])
					photo.save()
					return HttpResponseRedirect(Blog.redirect_route(blog_id=pk))
				except Exception as e:
					break

	else:
		form=PostCreateForm()
		formset=ImageFormset(queryset=PostImages.objects.none())

	context={
		'form':form,
		'formset':formset
	}
	return render(request,'blog/post_create.html',context)
