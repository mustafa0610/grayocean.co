from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import PostCreateView, PostUpdateView, PostDeleteView, UserBlogsList, not_creator, CommentList, comments_list, comment_delete, comment_detail,CommentDeleteView,about

urlpatterns=[
path('',views.BlogsList,name='blog-home'),
path('about',views.about,name='about'),
path('<int:blog_id>/like/', views.like_post, name='like_post'),
path('<int:blog_id>/dislike/', views.dislike_post, name='dislike_post'),
path('<int:blog_id>/report/', views.report_post, name='report_post'),
path('post/<int:pk>/', views.post_detail, name='post-detail'),
path('post/<int:blog_id>/all-comments', views.comments_list, name='post-comments'),
path('post/new/',PostCreateView.as_view(),name='post-create'),
path('post/<int:pk>/update/', PostUpdateView.as_view(),name ='post-update'),
path('post/<int:pk>/delete/', PostDeleteView.as_view(),name ='post-delete'),
path('user/<str:username>',UserBlogsList.as_view(),name='user-posts'),
path('profile/', views.profile, name='profile'),
path('accounts/login/', views.not_creator, name='cant_create'),
path('comment/<int:pk>/', views.comment_detail, name='comment'),
path('comment/<int:pk>/delete', views.comment_delete, name='comment-delete'),

]


if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 