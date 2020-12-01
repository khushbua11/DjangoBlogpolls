from .models import *
from .serializers import *
from rest_framework import viewsets

class QuestionViewSet(viewsets.ModelViewSet):
	serializer_class = QuestionSerializer
	queryset = Question.objects.all()
	# queryset = Question.objects.order_by('-id')
	http_method_names = ['get', 'post', 'patch', 'put', 'delete']

class ChoiceViewSet(viewsets.ModelViewSet):
	serializer_class = ChoiceSerializer
	queryset = Choice.objects.all()
	http_method_names = ['get', 'post', 'patch', 'put', 'delete']

