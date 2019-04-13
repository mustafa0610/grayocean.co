from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse 



class Blog(models.Model):
	title=models.CharField(max_length=100)
	content=models.TextField(blank=True)
	image = models.ImageField(upload_to='blog_images', blank=True)
	image1= models.ImageField(upload_to='blog_images', blank=True,verbose_name='second image')
	image2= models.ImageField(upload_to='blog_images', blank=True,verbose_name='third image')
	image3= models.ImageField(upload_to='blog_images', blank=True,verbose_name='fourth image')
	image4= models.ImageField(upload_to='blog_images', blank=True,verbose_name='fifth image')
	video =models.FileField(upload_to='blog_images',blank=True)
	date_posted=models.DateTimeField(default=timezone.now)
	author=models.ForeignKey(User, on_delete=models.CASCADE)
	likes=models.ManyToManyField(User,related_name='likes',blank=True)
	dislikes=models.ManyToManyField(User,related_name='dislikes',blank=True)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})

	def redirect_route(blog_id):
		return reverse('post-detail',args=[str(blog_id)])

	def to_comments(blog_id):
		return reverse('post-comments', args=[str(blog_id)])
	

class comment(models.Model):
	post=models.ForeignKey(Blog, on_delete=models.CASCADE)
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	content=models.TextField(max_length=160)
	timestamp=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.post.title,str(self.user.username))
	
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={"post_id": self. post_id, "comment_id": self.pk})

class Report(models.Model):
	post=models.ForeignKey(Blog, on_delete=models.CASCADE)
	user=models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return'{}-{}'.format(self.post.title,str(self.user.username))


class PostImages(models.Model):
	post=models.ForeignKey(Blog, on_delete=models.CASCADE)
	image=models.ImageField(upload_to='blog_images',blank=True)

	def __str__(self):
		return self.post.title + "image"