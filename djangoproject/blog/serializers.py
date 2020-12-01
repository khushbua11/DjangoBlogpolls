from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
	comment = serializers.SerializerMethodField()
	class Meta:
		model = Post
		fields = '__all__'

	def get_comment(self, obj):
		comments = Comment.objects.filter(post=obj.id).all()
		data = []
		for cmnt in comments:
			data.append({ 'name':cmnt.name, 'email':cmnt.email, 
						'body':cmnt.body,  'created_on':cmnt.created_on,
						'active':cmnt.active })
		return data

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Comment
		fields = '__all__'
