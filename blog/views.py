from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from .forms import ContactForm
from	django.shortcuts	import	redirect, render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect





# Create your views here.
def  post_list(request):
	posts = Post.objects.all()
	return render(request, 'blog/post_list.html', {'posts':posts})
def  post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})
def	post_new(request):
	if request.method == "POST":
		form	=	PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return	render(request,	'blog/post_edit.html',	{'form':	form})
def	post_edit(request,	pk):
	post	=	get_object_or_404(Post,	pk=pk)
	if	request.method	==	"POST":
		form	=	PostForm(request.POST,	instance=post)
		if	form.is_valid():
			post	=	form.save(commit=False)
			post.author	=	request.user
			post.published_date	=	timezone.now()
			post.save()
			return	redirect('post_detail',	pk=post.pk)
	else:
		form	=	PostForm(instance=post)
	return	render(request,	'blog/post_edit.html',	{'form':	form})
def about(request):
	return render(request, 'blog/about.html', {})

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            name = form.cleaned_data['name']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('sent')
    return render(request, "blog/contact.html", {'form': form})

def sent(request):
    return render(request, 'blog/sent.html', {})








