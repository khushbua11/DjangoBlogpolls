from rest_framework import serializers
from .models import *

class QuestionSerializer(serializers.ModelSerializer):
	choice = serializers.SerializerMethodField() # new field choice is defined in Question Serializer
	class Meta:
		model = Question
		fields = '__all__'

	def get_choice(self, obj):
		choices = Choice.objects.filter(question=obj.id).all()
		data = []
		for ch in choices:
			data.append({'id':ch.id, 'choice_text':ch.choice_text, 'votes':ch.votes})
		return data

class ChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Choice
		fields = '__all__'
