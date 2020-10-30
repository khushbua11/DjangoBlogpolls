from django.conf import settings
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.contrib import auth
from PIL import Image
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=200)
	slug = AutoSlugField(populate_from = 'name')

	def __str__(self):
		return self.name

status = [('Active','Active'),('Inactive', 'Inactive'), ('Drafted', 'Drafted')]

class Category(models.Model):
	title = models.CharField(max_length = 200)
	slug = AutoSlugField(populate_from = 'title')
	content = models.TextField()
	updated_time = models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length = 200, choices = status, default='Active')

	def publish(self):
		self.updated_time = timezone.now()
		self.save()

	def __str__(self):
		return self.title

class Post(models.Model):	
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
	tag = models.ManyToManyField(Tag, null=True)
	title = models.CharField(max_length = 200)
	slug = AutoSlugField(populate_from = 'title')
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)
	
	image = models.ImageField(upload_to =None, null=True)

	image_thumbnail = ImageSpecField (source = 'image', 
									processors = [ResizeToFill(100,50)], 
									format = 'JPEG',
									options = {'quality': 60} )

	# def my_slugify_function(content):
	# 	return content.replace('_', '-').lower()

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return ("/post/%s/" % self.slug)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	# manually deactivate inappropriate comments from admin site
	active = models.BooleanField(default=False)
	# parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True)

	class Meta:
		# sort comments in chronological order by default
		ordering = ['created_on']

	def __str__(self):
		return 'Comment {} by {}'.format(self.body, self.name)

class UserImage(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	profile_pic = models.ImageField(upload_to="userimage", blank=True)

	def __str__(self):
		return self.user.username


# class Thumbnail_image(models.Model):
# 	image = models.Imagefield(updatedto ='images/')
# 	title = models.CharField(max_length=80)
# 	summary = models.CharField(max_length=160)

# 	def _str_(self):
# 		return self.title