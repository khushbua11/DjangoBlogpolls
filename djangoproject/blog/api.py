from .models import *
from .serializers import *
from rest_framework import viewsets

class CategoryViewSet(viewsets.ModelViewSet):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()
	http_method_names = ['get', 'post', 'patch', 'put', 'delete']

class TagViewSet(viewsets.ModelViewSet):
	serializer_class = TagSerializer
	queryset = Tag.objects.all()
	http_method_names = ['get', 'post', 'patch', 'put', 'delete']

class PostViewSet(viewsets.ModelViewSet):
	serializer_class = PostSerializer
	queryset = Post.objects.order_by('-id')
	http_method_names = ['get', 'post', 'patch', 'put', 'delete']

class CommentViewSet(viewsets.ModelViewSet):
	serializer_class = CommentSerializer
	queryset = Comment.objects.all()
	http_method_names = ['get', 'post', 'patch', 'put', 'delete']
