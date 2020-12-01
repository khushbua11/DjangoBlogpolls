from . import views, api
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import renderers

router = DefaultRouter()
router.register('question', api.QuestionViewSet)
router.register('choice', api.ChoiceViewSet)

urlpatterns = [
		path('', include(router.urls)),
	]
