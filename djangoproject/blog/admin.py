from django.contrib import admin
from .models import Post, Tag, Category, Comment, UserImage

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug',)
	search_fields = ('title',)
	filter_horizontal = ('tag',)

class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug',)
	search_fields = ('name',)

class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'slug',)
	search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'body', 'post', 'created_on', 'active',)
	list_filter = ('active', 'created_on',)
	search_fields = ('name', 'email', 'body',)
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(active=True)

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserImage)
admin.site.register(Comment, CommentAdmin)
