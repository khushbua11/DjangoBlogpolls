from . import views, api
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import renderers

router = DefaultRouter()
router.register('category', api.CategoryViewSet)
router.register('tag', api.TagViewSet)
router.register('post', api.PostViewSet)
router.register('comment', api.CommentViewSet)

urlpatterns = [
		path('', include(router.urls)),
	]
