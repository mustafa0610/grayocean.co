def post_create(request):
	ImageFormset = modelformset_factory(PostImages, fields=('image',), extra=7)
	if request.method=='POST':
		form=PostCreateForm(request.POST)
		formset=ImageFormset(request.POST or None, request.FILES or None)
		if form.is_valid():
			post=form.save(commit=False)
			post.author=request.user
			post.save()
			pk=post.id
			return HttpResponseRedirect(Blog.redirect_route(blog_id=pk))
			# for f in formset:
			# 	try:
			# 		photo=PostImages(post=post,image=f.clean_data('image'))
			# 		photo.save()
			# 		return redirect('post-detail')
			# 	except Exception as e:
			# 		break
				
	else:
		form=PostCreateForm()
		formset=ImageFormset(queryset=PostImages.objects.none())

	context={
		'form':form,
		'formset':formset
	}
	return render(request,'blog/post_create.html',context)