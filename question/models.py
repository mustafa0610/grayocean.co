from django.db import models
from django.contrib.auth.models import User

class question(models.Model): 
	answer=models.TextField(blank=True)

	content=models.TextField(max_length=200) 

	timestamp=models.DateTimeField(auto_now_add=True) 

	user=models.ForeignKey(User,on_delete=models.CASCADE,default=0) 

	def __str__(self): 

	    return '{}-{}'.format(str(self.user.username),len(self.answer)) 