from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category, Tag, UserImage
from .forms import PostForm, CommentForm, ImageForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
#from mysite.core.forms import SignupForm

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
	# template_name = 'post_detail.html'
	post = get_object_or_404(Post, slug=slug)
	comments = post.comments.filter(active=True)
	new_comment = None
	# Comment posted
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():

			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			# Save the comment to the database
			new_comment.save()
	else:
		comment_form = CommentForm()

	return render(request, 'blog/post_detail.html', {'post': post,
										   'comments': comments,
										   'new_comment': new_comment,
										   'comment_form': comment_form})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog:post_detail', slug=post.slug)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
	post = get_object_or_404(Post, slug=slug)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('blog:post_detail', slug=post.slug)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def signup(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			# username = form.cleaned_data.get('username')
			# raw_password = form.cleaned_data.get('password1')
			# user = authenticate (username=username, password=raw_password)
			# login(request, user)
			messages.success(request, 'Account created successfully')
			return redirect('blog:signup')
			# return redirect('success')
	else:
		form = UserCreationForm()
	return render(request, 'blog/signup.html', {'form':form})

def logout(request):
	auth.logout(request)
	return render(request,'blog/logout.html')

# View function to show post related to Tag

def tag_list(request):
	tags = Tag.objects.all()
	return render(request, 'blog/tag_list.html', {'tags' : tags})

def tag_post_list(request, slug):
	tag = Tag.objects.get(slug=slug)
	posts = Post.objects.filter(tag=tag)
	context = { 'tag' : tag , 'posts' : posts }
	return render(request, 'blog/tag_post_list.html',  context )	

# View function to show post related to Category

def category_list(request):
	categorys = Category.objects.filter(updated_time__lte=timezone.now()).order_by('updated_time')
	return render(request, 'blog/category_list.html', {'categorys': categorys})

def category_post_list(request, slug):
	category = Category.objects.get(slug=slug)
	posts = Post.objects.filter(category=category).all()
	context = {'category' : category , 'posts' : posts}
	# print (context)
	return render(request, 'blog/category_post_list.html', context )	

def user_detail(request, pk):
	username = get_object_or_404(User, pk=pk)
	userimg = UserImage.objects.filter(user=request.user).first()
	return render(request, 'blog/user_detail.html', {'username':username, 'userimg': userimg }) 

# def user_detail(request, pk):
# 	user=get_object_or_404(User, pk=pk)
# 	if request.method == "GET":
# 		form = UserCreationForm(request.GET, instance=user)
# 		if form.is_valid():
# 			username = form.request.get('username')
# 			raw_password = form.request.get('password1')
# 			return username
# 			# return redirect(request, 'blog/user_detail.html', {'form':form}) 
# 	else:
# 		form = UserCreationForm()
# 	return render(request, 'blog/user_detail.html', {'form' : form})

def profile_edit(request, pk):
	user=get_object_or_404(User, pk=pk)
	if request.method == 'POST':
		form = UserProfileForm(request.POST, instance=user)
		img = ImageForm(request.POST, request.FILES)

		if form.is_valid() and img.is_valid():
			userimg = UserImage.objects.get(user=request.user)
			if userimg:
				userimg.profile_pic=img.cleaned_data.get('profile_pic')
				userimg.user=request.user
				userimg.save()
			else:
				form = form.save(commit=False)
				img = img.save(commit=False)
				form.user = request.user
				img.user = request.user
				userimg.save()
				form.save()
				img.save()
		return redirect('blog:user_detail', pk=user.pk)
	else:
		form = UserProfileForm(instance=user)
		img= ImageForm()
	return render(request, 'blog/profile_edit.html', {'form': form, 'img':img})

	def success(request): 
		return HttpResponse('successfully uploaded') 