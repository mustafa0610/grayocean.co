from django.contrib import admin
from .models import Blog, comment, Report, PostImages

admin.site.register(Blog)
admin.site.register(comment)
admin.site.register(Report)
admin.site.register(PostImages)
